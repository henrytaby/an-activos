import os
import pandas as pd
from typing import List, Dict, Any, Tuple, Set

class SafExcelExtractor:
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
        return [
            col.lower()
               .strip()
               .replace(' ', '')  # Quitar todos los espacios
               .replace('.', '')
               .replace(':', '')
            for col in columns
        ]

    def extract(self) -> Tuple[List[Dict[str, Any]], List[str]]:
        print(f"Buscando archivos Excel en la carpeta: {self.data_folder}")
        all_records = []
        processed_filenames = []

        try:
            available_files = [f for f in os.listdir(self.data_folder) if f.endswith(('.xlsx', '.xls')) and not f.startswith('~$')]
            files_to_process = [f for f in available_files if f not in self.processed_files]

            if not files_to_process:
                print("No hay archivos SAF nuevos para procesar.")
                return [], []
            
            print(f"Archivos SAF nuevos para procesar: {', '.join(files_to_process)}")

            for file_name in files_to_process:
                file_path = os.path.join(self.data_folder, file_name)
                print(f"Procesando archivo: {file_name}...")
                
                df = pd.read_excel(file_path, header=1, dtype=str).dropna(how='all')
                df.columns = self._normalize_columns(df.columns)

                # Limpieza específica para SAF
                if 'codigo' in df.columns:
                    df.dropna(subset=['codigo'], inplace=True)
                    df['codigo'] = df['codigo'].str.replace(' ', '')
                else:
                    print(f"Advertencia: El archivo {file_name} no tiene columna 'codigo'. Saltando archivo.")
                    continue

                if not df.empty:
                    processed_filenames.append(file_name)
                    for record in df.to_dict('records'):
                        clean_record = {k: (v if pd.notna(v) else None) for k, v in record.items()}
                        all_records.append(clean_record)

            return all_records, processed_filenames

        except Exception as e:
            print(f"Ocurrió un error inesperado durante la extracción SAF: {e}")
            return [], []
