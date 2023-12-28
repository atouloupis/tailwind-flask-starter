# testFile.py
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#from azure.identity import DefaultAzureCredential

# Remplacez ces valeurs par les vôtres
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")

# Utilisez DefaultAzureCredential pour l'authentification
blob_service_client = BlobServiceClient(
    account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
    credential=ACCOUNT_KEY,
)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Créer un "dossier" virtuel pour chaque profil
blob_prefix = f"test/"
 # Remplacez 'your_blob_name' par le nom que vous souhaitez donner au blob
blob_client = container_client.get_blob_client(blob_prefix + "your_blob_name")
# Téléchargez le fichier vers le blob
blob_client.upload_blob('test')
#echo('finished')

