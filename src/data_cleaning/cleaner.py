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

        print("--- Iniciando limpieza y llenado del campo 'institucion' ---")

        # Paso 1: Limpiar 'institucion' donde los códigos están vacíos
        print("Paso 1: Vaciando 'institucion' donde los códigos están vacíos...")
        query_empty = {
            "institucion": "ADUANA NACIONAL",
            "codigo_anterior": {"$in": [None, "", " "]},
            "codigo_nuevo": {"$in": [None, "", " "]}
        }
        update_empty = {"$set": {"institucion": ""}}
        result_empty = self.collection.update_many(query_empty, update_empty)
        print(f"Documentos con 'institucion' vaciada: {result_empty.modified_count}")

        # Paso 2: Llenar 'institucion' donde es necesario (lógica original)
        print("\nPaso 2: Llenando 'institucion' donde está vacío pero hay códigos...")
        query_fill = {
            "institucion": {"$in": [None, "", " "]},
            "$or": [
                {"codigo_anterior": {"$nin": [None, "", " "]}},
                {"codigo_nuevo": {"$nin": [None, "", " "]}}
            ]
        }
        update_fill = {"$set": {"institucion": "ADUANA NACIONAL"}}
        result_fill = self.collection.update_many(query_fill, update_fill)
        print(f"Documentos con 'institucion' rellenada: {result_fill.modified_count}")

        print("\n--- Resumen del proceso de 'institucion' ---")
        print(f"Total de documentos actualizados: {result_empty.modified_count + result_fill.modified_count}")
        print("Proceso de 'institucion' completado.")

    def clean_grupo(self):
        if not self.client:
            print("No se puede limpiar, no hay conexión a MongoDB.")
            return

        print("--- Iniciando limpieza del campo 'grupo' ---")
        
        mappings = settings.GRUPO_MAPPINGS
        if not mappings:
            print("No hay mapeos definidos para 'grupo' en la configuración. Finalizando.")
            return

        total_updated = 0
        for mapping in mappings:
            search_term = mapping.get("busqueda")
            replace_term = mapping.get("remplazar")

            if not search_term or not replace_term:
                continue

            query = {"grupo": search_term}
            cursor = self.collection.find(query)
            
            docs_to_update = list(cursor)
            if not docs_to_update:
                continue

            print(f"Procesando {len(docs_to_update)} documentos para el mapeo: '{search_term}' -> '{replace_term}'")

            for doc in docs_to_update:
                original_grupo = doc.get("grupo")
                original_descripcion = doc.get("descripcion", "")

                if original_descripcion:
                    new_descripcion = f"{original_grupo}, {original_descripcion}"
                else:
                    new_descripcion = original_grupo

                self.collection.update_one(
                    {"_id": doc["_id"]},
                    {
                        "$set": {
                            "grupo": replace_term,
                            "descripcion": new_descripcion
                        }
                    }
                )
                total_updated += 1
        
        print(f"\n--- Resumen de la limpieza de 'grupo' ---")
        print(f"Total de documentos actualizados: {total_updated}")
        print("Limpieza de 'grupo' completada.")

    @staticmethod
    def clean_data_values(data: list[dict]) -> list[dict]:
        """
        Limpia los datos en memoria, eliminando espacios en blanco al inicio y final
        de los valores de tipo string. Modifica los registros in-place.
        """
        if not data:
            return []

        for record in data:
            for key, value in record.items():
                if isinstance(value, str):
                    record[key] = value.strip()
        
        print(f"Se limpiaron {len(data)} registros en memoria (trimming).")
        return data

    def __del__(self):
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")
