#exportFile.py

# importFile.py
import os
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#from .models import files
from . import db    

exportFile = Blueprint('exportFile', __name__)

# Remplacez ces valeurs par les vôtres
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")


@exportFile.route("/export", methods=["GET"])
@login_required
def get_file():
    return jsonify({"error": "No file part"}), 400
