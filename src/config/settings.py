import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "activos_db")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "inventario")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
