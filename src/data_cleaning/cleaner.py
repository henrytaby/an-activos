from pymongo import MongoClient
from src.config import settings

class DataCleaner:
    def __init__(self):
        try:
            self.client = MongoClient(settings.MONGO_URI)
            self.db = self.client[settings.MONGO_DB_NAME]
            self.collection = self.db[settings.MONGO_COLLECTION_NAME]
            print("Conexión a MongoDB establecida para la limpieza.")
        except Exception as e:
            print(f"Error al conectar con MongoDB: {e}")
            self.client = None

    def clean_codigo_anterior(self):
        if not self.client:
            print("No se puede limpiar, no hay conexión a MongoDB.")
            return

        print("--- Iniciando limpieza del campo 'codigo_anterior' ---")
        query = {"codigo_anterior": {"$exists": True, "$ne": None}}
        cursor = self.collection.find(query)
        
        processed_count = 0
        updated_count = 0
        skipped_count = 0

        for doc in cursor:
            processed_count += 1
            original_code = doc.get("codigo_anterior")

            if not isinstance(original_code, str):
                original_code = str(original_code)

            # 1. Quitar espacios
            cleaned_code = original_code.replace(' ', '')

            # 2. Omitir si es muy largo
            if len(cleaned_code) > 10:
                print(f"ADVERTENCIA: Código '{original_code}' omitido por tener más de 10 dígitos.")
                skipped_count += 1
                continue
            
            # 3. Rellenar con ceros si es necesario (estándar de 9 dígitos)
            if len(cleaned_code) < 9:
                cleaned_code = cleaned_code.zfill(9)

            # 4. Actualizar solo si ha habido cambios
            if cleaned_code != original_code:
                self.collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"codigo_anterior": cleaned_code}}
                )
                updated_count += 1
        
        print("\n--- Resumen de la limpieza ---")
        print(f"Documentos procesados: {processed_count}")
        print(f"Documentos actualizados: {updated_count}")
        print(f"Documentos omitidos: {skipped_count}")
        print("Limpieza de 'codigo_anterior' completada.")

    def fill_institucion(self):
        if not self.client:
            print("No se puede procesar, no hay conexión a MongoDB.")
            return

        print("--- Iniciando llenado del campo 'institucion' ---")
        
        # Documentos donde 'institucion' está vacío o nulo
        # Y donde 'codigo_anterior' o 'codigo_nuevo' NO están vacíos o nulos.
        query = {
            "institucion": {"$in": [None, "", " "]},
            "$or": [
                {"codigo_anterior": {"$nin": [None, "", " "]}},
                {"codigo_nuevo": {"$nin": [None, "", " "]}}
            ]
        }

        update_action = {
            "$set": {"institucion": "ADUANA NACIONAL"}
        }

        result = self.collection.update_many(query, update_action)

        print("\n--- Resumen del llenado ---")
        print(f"Documentos actualizados: {result.modified_count}")
        print("Llenado de 'institucion' completado.")

    def __del__(self):
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")
