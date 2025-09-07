import os
import pandas as pd
import pytz
from typing import List, Dict, Any, Tuple, Set
from src.config import settings

class PersonaExcelExtractor:
    def __init__(self, data_folder: str, log_file_path: str):
        self.data_folder = data_folder
        self.log_file_path = log_file_path
        self.processed_files = self._load_processed_files()

    def _load_processed_files(self) -> Set[str]:
        try:
            with open(self.log_file_path, 'r') as f:
                return set(line.strip() for line in f)
        except FileNotFoundError:
            return set()

    def _normalize_columns(self, columns: pd.Index) -> list:
        return [col.lower().strip().replace(' ', '_') for col in columns]

    def extract(self) -> Tuple[List[Dict[str, Any]], List[str]]:
        print(f"Buscando archivos Excel en la carpeta: {self.data_folder}")
        all_records = []
        processed_filenames = []

        try:
            available_files = [f for f in os.listdir(self.data_folder) if f.endswith(('.xlsx', '.xls')) and not f.startswith('~$')]
            files_to_process = [f for f in available_files if f not in self.processed_files]

            if not files_to_process:
                print("No hay archivos de Persona nuevos para procesar.")
                return [], []
            
            print(f"Archivos de Persona nuevos para procesar: {', '.join(files_to_process)}")

            for file_name in files_to_process:
                file_path = os.path.join(self.data_folder, file_name)
                print(f"Procesando archivo: {file_name}...")
                
                # Leer desde la primera fila (header=0) y todo como texto para empezar
                df = pd.read_excel(file_path, header=0, dtype=str).dropna(how='all')
                df.columns = self._normalize_columns(df.columns)

                # --- Conversiones de Tipo Específicas ---
                # funcionarioId es la PK, si es inválida o falta, se omite la fila
                if 'funcionarioid' not in df.columns:
                    print(f"ERROR: El archivo {file_name} no tiene la columna 'funcionarioId'. Saltando archivo.")
                    continue
                df['funcionarioid'] = pd.to_numeric(df['funcionarioid'], errors='coerce')
                df.dropna(subset=['funcionarioid'], inplace=True)
                df['funcionarioid'] = df['funcionarioid'].astype(int)

                # Columnas numéricas
                for col in ['item', 'saf_id']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64') # Int64 soporta nulos
                
                if 'basico' in df.columns:
                    df['basico'] = pd.to_numeric(df['basico'], errors='coerce')

                # Columna de fecha
                if 'fecha_nacimiento' in df.columns:
                    s = pd.to_datetime(df['fecha_nacimiento'], format='%d/%m/%Y', errors='coerce')
                    try:
                        tz = pytz.timezone(settings.TIMEZONE)
                        # Localizar cada fecha válida individualmente, dejando las inválidas como None
                        df['fecha_nacimiento'] = s.apply(lambda dt: dt.tz_localize(tz) if pd.notna(dt) else None)
                    except pytz.UnknownTimeZoneError:
                        print(f"ADVERTENCIA: Zona horaria '{settings.TIMEZONE}' no encontrada. Las fechas se guardarán sin zona horaria.")
                        df['fecha_nacimiento'] = s.where(pd.notna(s), None)

                # Convertir a diccionarios y realizar una limpieza final explícita
                if not df.empty:
                    processed_filenames.append(file_name)
                    records = df.to_dict('records')
                    for record in records:
                        clean_record = {}
                        for key, value in record.items():
                            # pd.isna() es una función universal para detectar NaN, NaT, etc.
                            clean_record[key] = None if pd.isna(value) else value
                        all_records.append(clean_record)

            return all_records, processed_filenames

        except Exception as e:
            print(f"Ocurrió un error inesperado durante la extracción de Persona: {e}")
            return [], []
