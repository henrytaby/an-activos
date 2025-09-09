import typer
from typing_extensions import Annotated
from datetime import datetime
import pytz

from src.config import settings
from src.data_extraction.extractor import ExcelExtractor
from src.data_extraction.saf_extractor import SafExcelExtractor
from src.data_extraction.persona_extractor import PersonaExcelExtractor
from src.data_storage.writer import MongoWriter
from src.data_cleaning.cleaner import DataCleaner
from src.data_consolidation.consolidator import Consolidator

app = typer.Typer()

@app.command("extract", help="Extrae datos de activos (usuarios) y los carga en MongoDB.")
def run_extraction(
    data_folder: Annotated[str, typer.Option(help="Carpeta que contiene los archivos Excel.")] = "datos/usuarios"
):
    LOG_FILE = "datos/.processed_log.txt"
    print("--- INICIO DEL PROCESO DE EXTRACCIÓN DE ACTIVOS ---")
    extractor = ExcelExtractor(data_folder=data_folder, log_file_path=LOG_FILE)
    data, new_files_processed = extractor.extract()
    if not data:
        print("No se extrajeron nuevos datos. Finalizando.")
        return
    data = DataCleaner.clean_data_values(data)
    writer = MongoWriter()
    writer.write(data)
    if new_files_processed:
        with open(LOG_FILE, 'a') as f:
            for filename in new_files_processed:
                f.write(f"{filename}\n")
        print(f"Se registraron {len(new_files_processed)} archivos como procesados.")
    print("--- FIN DEL PROCESO ---")

@app.command("extract-saf", help="Extrae datos de SAF y los carga en MongoDB.")
def run_saf_extraction(
    data_folder: Annotated[str, typer.Option(help="Carpeta de archivos Excel de SAF.")] = "datos/saf"
):
    LOG_FILE = "datos/saf/.processed_log.txt"
    print("--- INICIO DEL PROCESO DE EXTRACCIÓN DE SAF ---")
    extractor = SafExcelExtractor(data_folder=data_folder, log_file_path=LOG_FILE)
    data, new_files_processed = extractor.extract()
    if not data:
        print("No se extrajeron nuevos datos de SAF. Finalizando.")
        return
    data = DataCleaner.clean_data_values(data)
    try:
        tz = pytz.timezone(settings.TIMEZONE)
        current_time = datetime.now(tz)
        for record in data:
            record['fecha_registro'] = current_time
    except pytz.UnknownTimeZoneError:
        current_time = datetime.now()
        for record in data:
            record['fecha_registro'] = current_time
    writer = MongoWriter(collection_name="saf")
    writer.write(data)
    if new_files_processed:
        with open(LOG_FILE, 'a') as f:
            for filename in new_files_processed:
                f.write(f"{filename}\n")
        print(f"Se registraron {len(new_files_processed)} archivos SAF como procesados.")
    print("--- FIN DEL PROCESO DE EXTRACCIÓN DE SAF ---")

@app.command("extract-persona", help="Extrae datos de personas y los carga en MongoDB.")
def run_persona_extraction(
    data_folder: Annotated[str, typer.Option(help="Carpeta de archivos Excel de Persona.")] = "datos/persona"
):
    LOG_FILE = "datos/persona/.processed_log.txt"
    print("--- INICIO DEL PROCESO DE EXTRACCIÓN DE PERSONA ---")
    extractor = PersonaExcelExtractor(data_folder=data_folder, log_file_path=LOG_FILE)
    data, new_files_processed = extractor.extract()
    if not data:
        print("No se extrajeron nuevos datos de Persona. Finalizando.")
        return
    data = DataCleaner.clean_data_values(data)
    
    # Asignar _id y añadir fecha_registro
    try:
        tz = pytz.timezone(settings.TIMEZONE)
        current_time = datetime.now(tz)
        for record in data:
            record['_id'] = record.pop('funcionarioid')
            record['fecha_registro'] = current_time
    except pytz.UnknownTimeZoneError:
        current_time = datetime.now()
        for record in data:
            record['_id'] = record.pop('funcionarioid')
            record['fecha_registro'] = current_time

    writer = MongoWriter(collection_name="persona")
    writer.write(data)

    if new_files_processed:
        with open(LOG_FILE, 'a') as f:
            for filename in new_files_processed:
                f.write(f"{filename}\n")
        print(f"Se registraron {len(new_files_processed)} archivos de Persona como procesados.")
    print("--- FIN DEL PROCESO DE EXTRACCIÓN DE PERSONA ---")

@app.command("clean", help="Ejecuta un proceso de limpieza sobre los datos en MongoDB.")
def run_cleaning(
    field: Annotated[str, typer.Argument(help="El campo a limpiar.")]
):
    cleaner = DataCleaner()
    if field == "codigo_anterior":
        cleaner.clean_codigo_anterior()
    elif field == "institucion":
        cleaner.fill_institucion()
    elif field == "grupo":
        cleaner.clean_grupo()
    else:
        print(f"Error: No hay limpieza definida para el campo '{field}'.")
        print("Campos disponibles: [codigo_anterior, institucion, grupo]")
    print("--- FIN DEL PROCESO DE LIMPIEZA ---")

@app.command("consolidate", help="Consolida los datos de SAF e Inventario en una nueva colección.")
def run_consolidation():
    consolidator = Consolidator()
    consolidator.consolidate()

if __name__ == "__main__":
    app()
