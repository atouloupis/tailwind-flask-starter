# importFile.py
import os,uuid,time,datetime, requests
from datetime import timedelta  
from flask import Blueprint, render_template, request, jsonify,flash,redirect,url_for,send_file, session
from flask_login import login_required,current_user
from sqlalchemy import select
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,generate_blob_sas, AccountSasPermissions
from . import db   
from .models import user,fileType,files,filesresidence


importFile = Blueprint('importFile', __name__)

# Remplacez ces valeurs par les vôtres
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")


@importFile.route('/upload', methods=["POST"])
@login_required
def upload():
    if "file" not in request.files:
        return jsonify({"status":"false","message":"Impossible à sauvegarder"})
    file = request.files["file"]
    residenceId=request.form.get('residence')
    fileTypeForm=eval(request.form.get('fileType'))
    if file.filename == "":
        return jsonify({"status":"false","message":"Merci d'ajouter un fichier valide"})
        
    # Utilisez DefaultAzureCredential pour l'authentification
    blob_service_client = BlobServiceClient(
        account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
        credential=ACCOUNT_KEY,
    )
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    for types in fileType:
        if types.name==fileTypeForm[0] :
            fileTypeResult=types

    # Générer un nom de fichier unique
    unique_filename = str(uuid.uuid4()) + "_" + file.filename
    # Créer un "dossier" virtuel pour chaque profil
    blob_prefix = f"residences/{residenceId}/{fileTypeResult.value}/"

    # Remplacez 'your_blob_name' par le nom que vous souhaitez donner au blob
    blob_client = container_client.get_blob_client(blob_prefix + unique_filename)

    # Téléchargez le fichier vers le blob
    blob_client.upload_blob(file)
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_file = files(
    fileName=request.form.get('name'),
    storageId=f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/"+blob_prefix+unique_filename,
    blobName=blob_prefix + unique_filename,
    userUpload = current_user.get_id(),
    fileType = fileTypeResult,
    metadataFile = '{}' 
    )

    # add the new file to the database
    db.session.add(new_file)
    db.session.commit()

    #Ajouter la correspondance fichier/residence en BDD
    new_fileresidence=filesresidence(
        filesId=new_file.id,
        residenceId=residenceId
    )
    db.session.add(new_fileresidence)
    db.session.commit()

    return jsonify({"status":"true","message":"Votre fichier a été enregistré."})


@importFile.route('/telecharger_fichier/<int:fileId>')
@login_required
def telecharger_fichier(fileId):
    currRes = session.get("currentRes")
    file_residence_query = select(filesresidence.residenceId,files.storageId,files.blobName,files.fileName)\
    .select_from(filesresidence)\
    .join(files,files.id==filesresidence.filesId)\
    .where(files.id == fileId)
    # Exécuter la requête et récupérer les résultats sous forme de liste
    file_residence = db.session.execute(file_residence_query).all()
    file_residence=[{"residenceId":member[0],"storageId":member[1],"blobName":member[2],"fileName":member[3]} for member in file_residence]
    if(file_residence[0]["residenceId"]==currRes["residenceId"]):
        BLOB_NAME=file_residence[0]["blobName"]
        url= file_residence[0]["storageId"]
        sas_token = generate_blob_sas(
            account_name=ACCOUNT_NAME,
            account_key=ACCOUNT_KEY,
            container_name=CONTAINER_NAME,
            blob_name=BLOB_NAME,
            permission=AccountSasPermissions(read=True),
            expiry=datetime.datetime.utcnow() + timedelta(hours=1)
        )
        url_with_sas = f"{url}?{sas_token}"
        response = requests.get(url_with_sas, stream=True)

        headers = {key: value for (key, value) in response.headers.items()}
        #return send_file(response.content)
        return (response.content, response.status_code, headers)
        #return redirect(url_with_sas)
    else:
        return redirect("www.google.com")
