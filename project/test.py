# testFile.py

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#from azure.identity import DefaultAzureCredential

# Remplacez ces valeurs par les vôtres
ACCOUNT_NAME = "geduser"
CONTAINER_NAME = "ged-immeuble"
ACCOUNT_KEY = "wVXm3NnLrB9IMLpB2jybrYXLNIE6stgUgLtTj7wDbhZWyzDijAHw6qGkt0Sfe5Zvt0+I3UjYiBi4+ASt5GApHg=="

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

