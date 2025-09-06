import typer
from typing_extensions import Annotated

from src.data_extraction.extractor import ExcelExtractor
from src.data_cleaning.cleaner import DataCleaner

app = typer.Typer()

@app.command("extract", help="Extrae datos de archivos Excel y los carga en MongoDB.")
def run_extraction(
    data_folder: Annotated[str, typer.Option(help="Carpeta que contiene los archivos Excel.")] = "datos/usuarios"
):
    """
    Comando para ejecutar el pipeline de extracción y carga de datos.
    """
    print("--- INICIO DEL PROCESO DE EXTRACCIÓN Y CARGA ---")
    
    extractor = ExcelExtractor(data_folder=data_folder)
    data = list(extractor.extract())

    if not data:
        print("No se extrajeron datos. Finalizando el proceso.")
        print("--- FIN DEL PROCESO ---")
        return

    print(f"Se extrajeron un total de {len(data)} registros válidos de todos los archivos.")

    writer = MongoWriter()
    writer.write(data)

    print("--- FIN DEL PROCESO ---")

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
    # Puedes añadir más sentencias 'elif' aquí para otros campos en el futuro
    # elif field == "otro_campo":
    #     cleaner.clean_otro_campo()
    else:
        print(f"Error: No hay un proceso de limpieza definido para el campo '{field}'.")
        print("Campos disponibles para limpieza: [codigo_anterior, institucion]")

    print("--- FIN DEL PROCESO DE LIMPIEZA ---")

if __name__ == "__main__":
    app()
