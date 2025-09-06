# Proyecto de Procesamiento de Activos

Este proyecto es una herramienta de línea de comandos (CLI) diseñada para extraer, limpiar, procesar y almacenar datos de activos fijos desde archivos Excel hacia una base de datos MongoDB. Su arquitectura modular y orientada a objetos permite una fácil expansión para futuras tareas de procesamiento y análisis.

## Características Principales

- **Extracción de Datos**: Lee múltiples archivos Excel de un directorio específico.
- **Limpieza y Estandarización**: Contiene módulos para limpiar y normalizar datos directamente en la base de datos (ej. formato de códigos, llenado de campos vacíos).
- **Base de Datos NoSQL**: Utiliza MongoDB para almacenar los datos, aprovechando su flexibilidad y escalabilidad.
- **Interfaz de Línea de Comandos**: Manejo de todas las funciones a través de comandos simples y claros, gracias a la librería Typer.
- **Configuración Centralizada**: Gestiona variables sensibles y de configuración (como la conexión a la base de datos) a través de un archivo `.env`.

## Estructura del Proyecto

El proyecto está organizado con una estructura clara para separar responsabilidades:

```
.an-activos/
├── datos/
│   └── usuarios/       # Directorio para los archivos Excel de entrada
├── src/                # Código fuente de la aplicación
│   ├── config/         # Lógica para cargar la configuración (.env)
│   ├── data_cleaning/  # Módulos para la limpieza de datos
│   ├── data_extraction/ # Módulos para la extracción de datos (Excel)
│   ├── data_storage/   # Módulos para la escritura de datos (MongoDB)
│   └── models/         # Definición de las estructuras de datos (ej. Activo)
├── venv/               # Entorno virtual de Python
├── .env                # Archivo de configuración local (NO subir a Git)
├── .env.example        # Plantilla para el archivo .env
├── .gitignore          # Archivos y carpetas ignorados por Git
├── main.py             # Punto de entrada de la aplicación CLI
├── requirements.txt    # Lista de dependencias de Python
└── README.md           # Este archivo
```

## Configuración e Instalación

Sigue estos pasos para poner en marcha el proyecto.

### Prerrequisitos

- Python 3.8 o superior.
- Una instancia de MongoDB en ejecución.

### Pasos de Instalación

1.  **Clonar el Repositorio** (si está en un control de versiones como Git):
    ```bash
    git clone <url-del-repositorio>
    cd an-activos
    ```

2.  **Crear y Activar un Entorno Virtual**:
    ```bash
    # Crear el entorno
    python -m venv venv

    # Activar en Windows
    .\venv\Scripts\activate

    # Activar en macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar Dependencias**:
    Asegúrate de que tu entorno virtual esté activado y luego ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno**:
    - Crea una copia del archivo `.env.example` y renómbrala a `.env`.
    - Abre el archivo `.env` y modifica las variables según tu configuración local de MongoDB.
    ```ini
    # Ejemplo de contenido para .env
    MONGO_URI="mongodb://localhost:27017/"
    MONGO_DB_NAME="activos_db"
    MONGO_COLLECTION_NAME="inventario"
    ```

## Modo de Uso

Todas las operaciones se realizan a través de `main.py`.

### 1. Colocar los Archivos de Datos

Copia todos los archivos Excel que deseas procesar dentro de la carpeta `datos/usuarios/`.

### 2. Extracción de Datos

Este comando lee todos los archivos Excel de la carpeta de datos, los procesa en memoria y los carga en la colección de MongoDB especificada en tu archivo `.env`.

```bash
python main.py extract
```

### 3. Limpieza de Datos

El comando `clean` modifica los datos que ya se encuentran en la base de datos. Debes especificar qué campo quieres limpiar.

- **Limpiar y estandarizar `codigo_anterior`**:
  Este proceso elimina espacios y rellena con ceros a la izquierda hasta tener 9 dígitos.
  ```bash
  python main.py clean codigo_anterior
  ```

- **Rellenar el campo `institucion`**:
  Este proceso llena el campo `institucion` con "ADUANA NACIONAL" en los registros donde este campo esté vacío pero que tengan un código de activo.
  ```bash
  python main.py clean institucion
  ```
