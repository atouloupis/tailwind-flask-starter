# importFile.py
import os,uuid,time
from flask import Blueprint, render_template, request, jsonify,flash,redirect,url_for
from flask_login import login_required,current_user
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#from .models import files
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
    print(file.filename)
    #print(list(map(lambda c: c.value, fileType)))
    residenceId=request.form.get('residence')
    fileTypeForm=eval(request.form.get('fileType'))
    #print("filetype."+fileTypeForm[0])
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
            print(fileTypeResult)

    # Générer un nom de fichier unique
    unique_filename = str(uuid.uuid4()) + "_" + file.filename
    # Créer un "dossier" virtuel pour chaque profil
    blob_prefix = f"residences/{residenceId}/{fileTypeResult.value}/"

    # Remplacez 'your_blob_name' par le nom que vous souhaitez donner au blob
    blob_client = container_client.get_blob_client(blob_prefix + unique_filename)

    # Téléchargez le fichier vers le blob
    #blob_client.upload_blob(file)
    #print(blob_client.url)
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_file = files(
    storageId=blob_client.url,
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
