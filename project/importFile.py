# importFile.py
import os
import uuid
from flask import Blueprint, render_template, request, jsonify,flash,redirect,url_for
from flask_login import login_required,current_user
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#from .models import files
from . import db   
from .models import user 

importFile = Blueprint('importFile', __name__)

# Remplacez ces valeurs par les vôtres
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")
print(ACCOUNT_KEY)


@importFile.route("/upload", methods=["POST"])
@login_required
def upload_file():
    print(current_user)
    if "file" not in request.files:
        flash('Impossible à sauvegarder')
        return redirect(request.referrer or url_for('main.tourdecontrol'))

    file = request.files["file"]
    residenceId=request.form.get('residence')

    if file.filename == "":
        flash('Pas de fichier sauvegardé')
        return redirect(request.referrer or url_for('main.tourdecontrol'))

    # Utilisez DefaultAzureCredential pour l'authentification
    blob_service_client = BlobServiceClient(
        account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
        credential=ACCOUNT_KEY,
    )
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    
    # Générer un nom de fichier unique
    unique_filename = str(uuid.uuid4()) + "_" + file.filename
    # Créer un "dossier" virtuel pour chaque profil
    blob_prefix = f"{residenceId}/"

    # Remplacez 'your_blob_name' par le nom que vous souhaitez donner au blob
    blob_client = container_client.get_blob_client(blob_prefix + unique_filename)

    # Téléchargez le fichier vers le blob
    blob_client.upload_blob(file)

    flash('Fichier sauvegardé')
    return redirect(url_for('main.tourdecontrol'))
