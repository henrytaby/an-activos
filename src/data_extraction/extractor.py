import os
import pandas as pd
from typing import Iterator, Dict, Any

class ExcelExtractor:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder

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

    def extract(self) -> Iterator[Dict[str, Any]]:
        print(f"Buscando archivos Excel en la carpeta: {self.data_folder}")
        try:
            files = [
                f for f in os.listdir(self.data_folder) 
                if f.endswith(('.xlsx', '.xls')) and not f.startswith('~$')
            ]
            if not files:
                print(f"Advertencia: No se encontraron archivos Excel en la carpeta '{self.data_folder}'.")
                return
            
            print(f"Archivos encontrados: {', '.join(files)}")

            for file_name in files:
                file_path = os.path.join(self.data_folder, file_name)
                print(f"Procesando archivo: {file_name}...")
                
                df = pd.read_excel(file_path, header=1, dtype=str)

                # --- INICIO DE TRANSFORMACIONES ---

                # 1. Normalizar y renombrar columnas
                df.columns = self._normalize_columns(df.columns)
                df.rename(columns={'anterior': 'codigo_anterior', 'nuevo': 'codigo_nuevo'}, inplace=True)

                # 2. Limpiar 'S/C' en columnas de código
                if 'codigo_anterior' in df.columns:
                    df['codigo_anterior'] = df['codigo_anterior'].apply(self._clean_sc)
                if 'codigo_nuevo' in df.columns:
                    df['codigo_nuevo'] = df['codigo_nuevo'].apply(self._clean_sc)

                # 3. Crear la columna 'encargado' a partir de 'asignado_a'
                if 'asignado_a' in df.columns:
                    df['encargado'] = df['asignado_a']
                else:
                    df['encargado'] = None

                # 4. Convertir columnas a tipo booleano
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

                # 5. Dejar 'asignado_a' en blanco si 'saf' es False
                if 'asignado_a' in df.columns:
                    df.loc[df['saf'] == False, 'asignado_a'] = None
                
                # --- FIN DE TRANSFORMACIONES ---

                if 'nro' not in df.columns:
                    print(f"Advertencia: El archivo {file_name} no tiene columna 'nro'. Saltando archivo.")
                    continue

                df['nro'] = pd.to_numeric(df['nro'], errors='coerce')
                df.dropna(subset=['nro'], inplace=True)
                df['nro'] = df['nro'].astype(int)

                df['archivo'] = file_name
                
                df = df.where(pd.notna(df), None)

                for record in df.to_dict('records'):
                    # Reemplazar cualquier valor tipo NaN (np.nan, pd.NA, etc.) con None para compatibilidad con BSON
                    yield {k: (v if pd.notna(v) else None) for k, v in record.items()}

        except FileNotFoundError:
            print(f"Error: La carpeta '{self.data_folder}' no fue encontrada.")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la extracción: {e}")