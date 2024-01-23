# importFile.py
import os,uuid,time,datetime
from datetime import timedelta  
from flask import Blueprint, render_template, request, jsonify,flash,redirect,url_for,send_file
from flask_login import login_required,current_user
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


@importFile.route('/telecharger_fichier')
def telecharger_fichier():
    BLOB_NAME='residences/1/Estimation/2d36b20a-ea61-4522-9ae3-61b4502b0c0f_Roadmap SI - P1.pdf'
    url='https://geduser.blob.core.windows.net/ged-immeuble/residences/1/Estimation/2d36b20a-ea61-4522-9ae3-61b4502b0c0f_Roadmap SI - P1.pdf'
    sas_token = generate_blob_sas(
        account_name=ACCOUNT_NAME,
        account_key=ACCOUNT_KEY,
        container_name=CONTAINER_NAME,
        blob_name=BLOB_NAME,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.datetime.utcnow() + timedelta(hours=1)
    )

    url_with_sas = f"{url}?{sas_token}"
    return redirect(url_with_sas)
