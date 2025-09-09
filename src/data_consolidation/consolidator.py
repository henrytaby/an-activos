from pymongo import MongoClient
from typing import List, Dict, Any
from datetime import datetime
import pytz

from src.config import settings
from src.data_storage.writer import MongoWriter
from src.models.activo_consolidado import ActivoConsolidado

class Consolidator:
    def __init__(self):
        try:
            self.client = MongoClient(settings.MONGO_URI)
            self.db = self.client[settings.MONGO_DB_NAME]
            self.saf_collection = self.db["saf"]
            self.inventario_collection = self.db["inventario"]
            self.consolidado_collection_name = "activos_consolidado"
            self.consolidado_collection = self.db[self.consolidado_collection_name]
            print("Conexión a MongoDB establecida para consolidación.")
        except Exception as e:
            print(f"Error al conectar con MongoDB: {e}")
            self.client = None

    def consolidate(self):
        if not self.client:
            print("No se puede consolidar, no hay conexión a MongoDB.")
            return

        print("--- INICIO DEL PROCESO DE CONSOLIDACIÓN ---")
        
        # Limpiar colección consolidada existente
        self.consolidado_collection.delete_many({})
        print(f"Colección '{self.consolidado_collection_name}' limpiada.")

        # Procesar Grupo 1
        activos_grupo_1, saf_codigos_procesados = self._procesar_grupo_1()

        # Procesar Grupo 2
        activos_grupo_2 = self._procesar_grupo_2(saf_codigos_procesados)

        # Combinar y escribir datos
        activos_consolidados = activos_grupo_1 + activos_grupo_2
        
        if activos_consolidados:
            writer = MongoWriter(collection_name=self.consolidado_collection_name)
            writer.write([activo.to_dict() for activo in activos_consolidados])
        else:
            print("No se generaron datos consolidados.")

        print(f"--- FIN DEL PROCESO DE CONSOLIDACIÓN ---")
        print(f"Total de activos consolidados: {len(activos_consolidados)}")
        print(f"- {len(activos_grupo_1)} activos del GRUPO 1")
        print(f"- {len(activos_grupo_2)} activos del GRUPO 2")

    def _procesar_grupo_1(self) -> (List[ActivoConsolidado], List[str]):
        print("Procesando GRUPO 1...")
        pipeline = [
            {
                "$match": {
                    "responsable": {
                        "$nin": [
                            "ZELADA GUARACHI RONALD",
                            "URQUIDI SALMON JOSE PASTOR",
                            "RIOS JARAMILLO JORGE",
                            "MIRANDA CHAVEZ MARISOL",
                            "MENDIZABAL PACHECO AUGUSTO",
                            "LIMA LLUSCO JULIO CESAR",
                            "DIAZ CAMACHO ALISSON ALEJANDRA",
                            "ABAN ARAMAYO OMAR"
                        ]
                    }
                }
            },
            {
                "$lookup": {
                    "from": "inventario",
                    "localField": "codigo",
                    "foreignField": "codigo_anterior",
                    "as": "registros_inventario"
                }
            },
            {
                "$project": {
                    "codigo": 1,
                    "anterior": 1,
                    "grupo": 1,
                    "descripcion": 1,
                    "estadousoactivo": 1,
                    "estadoactivo": 1,
                    "proyecto": 1,
                    "responsable": 1,
                    "fecha_registro": 1,
                    "registros_inventario": 1
                }
            }
        ]

        saf_activos = list(self.saf_collection.aggregate(pipeline))
        activos_consolidados = []
        saf_codigos_procesados = []

        for saf_activo in saf_activos:
            saf_codigos_procesados.append(saf_activo.get("codigo"))
            registros_inventario = saf_activo.get("registros_inventario", [])

            # Lógica para obtener el primer valor no nulo
            def get_first_value(field):
                for reg in registros_inventario:
                    if reg.get(field):
                        return reg.get(field)
                return None

            # Lógica para concatenar valores
            def concat_values(field):
                values = [reg.get(field) for reg in registros_inventario if reg.get(field)]
                return ", ".join(values)

            # Lógica para 'any' booleano
            def any_true(field):
                return any(reg.get(field) for reg in registros_inventario)

            try:
                tz = pytz.timezone(settings.TIMEZONE)
                fecha_registro = datetime.now(tz)
            except pytz.UnknownTimeZoneError:
                fecha_registro = datetime.now()

            activo = ActivoConsolidado(
                codigo_anterior=saf_activo.get("codigo"),
                codigo_nuevo=get_first_value("codigo_nuevo"),
                nroacta=get_first_value("nroacta"),
                grupo=get_first_value("grupo"),
                descripcion=saf_activo.get("descripcion"),
                serie=get_first_value("serie"),
                estado_uso_activo=get_first_value("estado_uso_activo"),
                area=get_first_value("area"),
                ubicacion=get_first_value("ubicacion"),
                asignado_a=saf_activo.get("responsable"),
                observacion=concat_values("observacion"),
                saf=True,
                verificado_fisicamente=any_true("verificado_fisicamente"),
                dar_baja=any_true("dar_baja"),
                institucion=get_first_value("institucion"),
                fecha_registro=fecha_registro,
                encargado=get_first_value("encargado"),
                archivo=concat_values("archivo")
            )
            activos_consolidados.append(activo)
        
        print(f"- Encontrados {len(saf_activos)} activos en SAF para procesar.")
        print(f"- Generados {len(activos_consolidados)} activos consolidados del GRUPO 1.")
        return activos_consolidados, saf_codigos_procesados

    def _procesar_grupo_2(self, saf_codigos_procesados: List[str]) -> List[ActivoConsolidado]:
        print("Procesando GRUPO 2...")
        inventario_activos = list(self.inventario_collection.find({
            "codigo_anterior": {"$nin": saf_codigos_procesados}
        }))

        activos_consolidados = []
        for inv_activo in inventario_activos:
            activo = ActivoConsolidado(
                codigo_anterior=inv_activo.get("codigo_anterior"),
                codigo_nuevo=inv_activo.get("codigo_nuevo"),
                nroacta=inv_activo.get("nroacta"),
                grupo=inv_activo.get("grupo"),
                descripcion=inv_activo.get("descripcion"),
                serie=inv_activo.get("serie"),
                estado_uso_activo=inv_activo.get("estado_uso_activo"),
                area=inv_activo.get("area"),
                ubicacion=inv_activo.get("ubicacion"),
                asignado_a=inv_activo.get("asignado_a"),
                observacion=inv_activo.get("observacion"),
                saf=inv_activo.get("saf", False),
                verificado_fisicamente=inv_activo.get("verificado_fisicamente", False),
                dar_baja=inv_activo.get("dar_baja", False),
                institucion=inv_activo.get("institucion"),
                fecha_registro=inv_activo.get("fecha_registro"),
                encargado=inv_activo.get("encargado"),
                archivo=inv_activo.get("archivo")
            )
            activos_consolidados.append(activo)

        print(f"- Encontrados {len(inventario_activos)} activos en 'inventario' para el GRUPO 2.")
        return activos_consolidados

    def __del__(self):
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")
