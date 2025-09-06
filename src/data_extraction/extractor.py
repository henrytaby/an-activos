import os
import pandas as pd
from typing import Iterator, Dict, Any, Tuple, List, Set

class ExcelExtractor:
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
               .replace(' ', '_')
               .replace('.', '')
               .replace(':', '')
               .replace('¿', '')
               .replace('?', '')
               .replace('ó', 'o')
               .replace('í', 'i')
            for col in columns
        ]

    def _clean_sc(self, value):
        if isinstance(value, str) and value.strip().lower() == 's/c':
            return None
        return value

    def extract(self) -> Tuple[List[Dict[str, Any]], List[str]]:
        print(f"Buscando archivos Excel en la carpeta: {self.data_folder}")
        all_records = []
        processed_filenames = []

        try:
            available_files = [
                f for f in os.listdir(self.data_folder) 
                if f.endswith(('.xlsx', '.xls')) and not f.startswith('~$')
            ]

            # Filtrar archivos que ya han sido procesados
            files_to_process = [f for f in available_files if f not in self.processed_files]

            if not files_to_process:
                print("No hay archivos nuevos para procesar.")
                return [], []
            
            print(f"Archivos nuevos para procesar: {', '.join(files_to_process)}")

            for file_name in files_to_process:
                file_path = os.path.join(self.data_folder, file_name)
                print(f"Procesando archivo: {file_name}...")
                
                df = pd.read_excel(file_path, header=1, dtype=str)
                
                # --- INICIO DE TRANSFORMACIONES ---
                df.columns = self._normalize_columns(df.columns)
                df.rename(columns={'anterior': 'codigo_anterior', 'nuevo': 'codigo_nuevo'}, inplace=True)
                if 'codigo_anterior' in df.columns:
                    df['codigo_anterior'] = df['codigo_anterior'].apply(self._clean_sc)
                if 'codigo_nuevo' in df.columns:
                    df['codigo_nuevo'] = df['codigo_nuevo'].apply(self._clean_sc)
                if 'asignado_a' in df.columns:
                    df['encargado'] = df['asignado_a']
                else:
                    df['encargado'] = None
                def to_bool(series, true_value):
                    return series.fillna('').astype(str).str.strip().str.lower() == true_value.lower()
                if 'estado_activo' in df.columns:
                    df['estado_activo'] = to_bool(df['estado_activo'], 'activo')
                if 'saf' in df.columns:
                    df['saf'] = to_bool(df['saf'], 'si')
                else:
                    df['saf'] = False
                if 'verificado_fisicamente' in df.columns:
                    df['verificado_fisicamente'] = to_bool(df['verificado_fisicamente'], 'si')
                if 'dar_baja' in df.columns:
                    df['dar_baja'] = to_bool(df['dar_baja'], 'si')
                if 'asignado_a' in df.columns:
                    df.loc[df['saf'] == False, 'asignado_a'] = None
                if 'nro' not in df.columns:
                    print(f"Advertencia: El archivo {file_name} no tiene columna 'nro'. Saltando archivo.")
                    processed_filenames.append(file_name) # Marcar como procesado aunque se omita
                    continue
                df['nro'] = pd.to_numeric(df['nro'], errors='coerce')
                df.dropna(subset=['nro'], inplace=True)
                df['nro'] = df['nro'].astype(int)
                df['archivo'] = file_name
                df = df.where(pd.notna(df), None)
                # --- FIN DE TRANSFORMACIONES ---

                # Añadir a la lista de procesados solo si tuvo datos válidos
                if not df.empty:
                    processed_filenames.append(file_name)
                    for record in df.to_dict('records'):
                        clean_record = {k: (v if pd.notna(v) else None) for k, v in record.items()}
                        all_records.append(clean_record)
                else:
                    print(f"Advertencia: El archivo {file_name} no contenía registros válidos después de la limpieza.")
                    # También lo marcamos como procesado para no reintentarlo
                    processed_filenames.append(file_name)

            return all_records, processed_filenames

        except FileNotFoundError:
            print(f"Error: La carpeta '{self.data_folder}' no fue encontrada.")
            return [], []
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la extracción: {e}")
            return [], []
