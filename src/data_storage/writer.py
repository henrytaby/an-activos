from pymongo import MongoClient
from typing import List, Dict, Any
from src.config import settings

class MongoWriter:
    def __init__(self, collection_name: str = None):
        try:
            self.client = MongoClient(settings.MONGO_URI)
            self.db = self.client[settings.MONGO_DB_NAME]
            # Usar la colección proporcionada o la de por defecto de la configuración
            _collection = collection_name or settings.MONGO_COLLECTION_NAME
            self.collection = self.db[_collection]
            print(f"Conexión a MongoDB establecida. Colección: '{_collection}'.")
        except Exception as e:
            print(f"Error al conectar con MongoDB: {e}")
            self.client = None

    def write(self, data: List[Dict[str, Any]]):
        if not self.client:
            print("No se pueden escribir los datos, no hay conexión a MongoDB.")
            return

        if not data:
            print("No hay datos para escribir en la base de datos.")
            return

        print(f"Insertando {len(data)} registros en la colección '{self.collection.name}'...")
        try:
            self.collection.insert_many(data)
            print("Datos insertados correctamente.")
        except Exception as e:
            print(f"Error al insertar datos en MongoDB: {e}")

    def __del__(self):
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")
