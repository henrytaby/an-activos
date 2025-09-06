import typer
from typing_extensions import Annotated
from datetime import datetime
import pytz

from src.config import settings
from src.data_extraction.extractor import ExcelExtractor
from src.data_extraction.saf_extractor import SafExcelExtractor
from src.data_storage.writer import MongoWriter
from src.data_cleaning.cleaner import DataCleaner

app = typer.Typer()

@app.command("extract", help="Extrae datos de archivos Excel nuevos y los carga en MongoDB.")
def run_extraction(
    data_folder: Annotated[str, typer.Option(help="Carpeta que contiene los archivos Excel.")] = "datos/usuarios"
):
    """
    Comando para ejecutar el pipeline de extracción y carga de datos.
    """
    LOG_FILE = "datos/.processed_log.txt"
    print("--- INICIO DEL PROCESO DE EXTRACCIÓN Y CARGA ---")
    
    extractor = ExcelExtractor(data_folder=data_folder, log_file_path=LOG_FILE)
    data, new_files_processed = extractor.extract()

    if not data:
        print("No se extrajeron nuevos datos. Finalizando el proceso.")
        print("--- FIN DEL PROCESO ---")
        return

    print(f"Se extrajeron un total de {len(data)} registros válidos de los archivos nuevos.")

    writer = MongoWriter() # Usa la colección por defecto de .env
    writer.write(data)

    if new_files_processed:
        try:
            with open(LOG_FILE, 'a') as f:
                for filename in new_files_processed:
                    f.write(f"{filename}\n")
            print(f"Se registraron {len(new_files_processed)} archivos como procesados.")
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo escribir en el archivo de registro: {e}")

    print("--- FIN DEL PROCESO ---")

@app.command("extract-saf", help="Extrae datos desde los archivos de SAF y los carga en MongoDB.")
def run_saf_extraction(
    data_folder: Annotated[str, typer.Option(help="Carpeta que contiene los archivos Excel de SAF.")] = "datos/saf"
):
    """
    Comando para el pipeline de extracción de datos de SAF.
    """
    LOG_FILE = "datos/saf/.processed_log.txt"
    print("--- INICIO DEL PROCESO DE EXTRACCIÓN DE SAF ---")
    
    extractor = SafExcelExtractor(data_folder=data_folder, log_file_path=LOG_FILE)
    data, new_files_processed = extractor.extract()

    if not data:
        print("No se extrajeron nuevos datos de SAF. Finalizando el proceso.")
        return

    # Añadir fecha de registro
    try:
        tz = pytz.timezone(settings.TIMEZONE)
        current_time = datetime.now(tz)
        for record in data:
            record['fecha_registro'] = current_time
    except pytz.UnknownTimeZoneError:
        print(f"ADVERTENCIA: Zona horaria '{settings.TIMEZONE}' no encontrada. Se usará la hora del sistema.")
        current_time = datetime.now()
        for record in data:
            record['fecha_registro'] = current_time

    # Guardar en la colección 'saf'
    writer = MongoWriter(collection_name="saf")
    writer.write(data)

    # Registrar archivos procesados
    if new_files_processed:
        try:
            with open(LOG_FILE, 'a') as f:
                for filename in new_files_processed:
                    f.write(f"{filename}\n")
            print(f"Se registraron {len(new_files_processed)} archivos SAF como procesados.")
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo escribir en el archivo de registro de SAF: {e}")

    print("--- FIN DEL PROCESO DE EXTRACCIÓN DE SAF ---")

@app.command("clean", help="Ejecuta un proceso de limpieza sobre los datos en MongoDB.")
def run_cleaning(
    field: Annotated[str, typer.Argument(help="El campo de la base de datos que se quiere limpiar.")]
):
    """
    Comando para ejecutar tareas de limpieza de datos.
    """
    cleaner = DataCleaner()
    
    if field == "codigo_anterior":
        cleaner.clean_codigo_anterior()
    elif field == "institucion":
        cleaner.fill_institucion()
    else:
        print(f"Error: No hay un proceso de limpieza definido para el campo '{field}'.")
        print("Campos disponibles para limpieza: [codigo_anterior, institucion]")

    print("--- FIN DEL PROCESO DE LIMPIEZA ---")

if __name__ == "__main__":
    app()