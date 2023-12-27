# importFile.py
import os
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#from .models import files
from . import db    

importFile = Blueprint('importFile', __name__)

# Remplacez ces valeurs par les vôtres
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")


@importFile.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    residenceId=request.form.get('residence')

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Utilisez DefaultAzureCredential pour l'authentification
    blob_service_client = BlobServiceClient(
        account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
        credential=ACCOUNT_KEY,
    )
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    # Créer un "dossier" virtuel pour chaque profil
    blob_prefix = f"{residenceId}/"

    # Remplacez 'your_blob_name' par le nom que vous souhaitez donner au blob
    blob_client = container_client.get_blob_client(blob_prefix + file.filename)

    # Téléchargez le fichier vers le blob
    blob_client.upload_blob(file)

    return jsonify({"message": "File uploaded successfully"}), 200
