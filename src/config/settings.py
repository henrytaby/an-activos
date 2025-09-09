import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "activos_db")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "inventario")
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Mapeos para la limpieza del campo 'grupo'
GRUPO_MAPPINGS = [
    {"busqueda": "SILLA PARA EL USUARIO", "remplazar": "SILLA"},
    {"busqueda": "ESCRITORIOS", "remplazar": "ESCRITORIO"},
    {"busqueda": "ESCRITORIO DE OFICINA", "remplazar": "ESCRITORIO"},
    {"busqueda": "ESCRITORIO CON VIDRIO 3 PIEZAS", "remplazar": "ESCRITORIO"},
    
    {"busqueda": "ESTANTE METALICO", "remplazar": "ESTANTE"},
    {"busqueda": "MUEBLES", "remplazar": "MUEBLE"},
    {"busqueda": "MUEBLES Y ENSERES", "remplazar": "MUEBLE"},
    {"busqueda": "SILLAS METALICAS DE ESPERA", "remplazar": "SILLA"},
    {"busqueda": "POSTE UNIFILAR BASTON CON BASE PLATEADA", "remplazar": "POSTE UNIFILAR"},
    {"busqueda": "SWICH", "remplazar": "SWITCH"},

    {"busqueda": "SILLA DE ESPERA", "remplazar": "SILLA"},
    {"busqueda": "SILLA GIRATORIA", "remplazar": "SILLA"},
    {"busqueda": "SILLAS", "remplazar": "SILLA"},
    {"busqueda": "SILLAS DE OFICINA", "remplazar": "SILLA"},
    {"busqueda": "SCANER", "remplazar": "SCANNER"},
    {"busqueda": "QUIPUS", "remplazar": "CPU"},
    {"busqueda": "MUEBLE BUZON RECLAMOS", "remplazar": "MUEBLE"},
    {"busqueda": "MUEBLE PARA COMPUTADORA", "remplazar": "MUEBLE"},
    
    {"busqueda": "INTERCRON", "remplazar": "INTERCOMUNICADOR"},

    {"busqueda": "CAMILLA DE EXAMEN", "remplazar": "CAMILLA"},
    {"busqueda": "COLCHONES", "remplazar": "COLCHON"},
    {"busqueda": "DISPENSADOR", "remplazar": "DISPENSADOR DE AGUA"},
    {"busqueda": "DISPENSADORDE AGUA", "remplazar": "DISPENSADOR DE AGUA"},
    {"busqueda": "BEBEDERO E AGUA", "remplazar": "DISPENSADOR DE AGUA"},
    
    {"busqueda": "IMPRESORA A LASER", "remplazar": "IMPRESORA"},
    {"busqueda": "MEZON DE METAL", "remplazar": "MESON"},
    {"busqueda": "GABETERO", "remplazar": "GAVETERO"},
    {"busqueda": "UPS TRIPP-LITE", "remplazar": "UPS"},
    {"busqueda": "TELEVISOR LED", "remplazar": "TELEVISOR"},
    {"busqueda": "SILLA GIRATORIA EN TAPIZ", "remplazar": "SILLA"},
    {"busqueda": "APARATO TELÉFONO", "remplazar": "TELEFONO"},
    {"busqueda": "RELOJ BIOMETRICO", "remplazar": "EQUIPO BIOMETRICO"},
    {"busqueda": "TELÉFONO", "remplazar": "TELEFONO"},
    {"busqueda": "TUBO DE OXÍGENO", "remplazar": "TUBO DE OXIGENO"},

    {"busqueda": "VITRINA DE MADERA", "remplazar": "VITRINA"},

    {"busqueda": "CAMAROTE METALICO", "remplazar": "CAMAROTE"},
    {"busqueda": "CAMAROTE METALICO.", "remplazar": "CAMAROTE"},
    {"busqueda": "CUCHETA", "remplazar": "CAMAROTE"},
    {"busqueda": "LAVADORAS", "remplazar": "LAVADORA"},
    {"busqueda": "MESA DE MADERA", "remplazar": "MESA"},  
     
]

# Mapeos para la limpieza del campo 'institucion'
INSTITUCION_MAPPINGS = [
    {"busqueda": "ADUANA BOLIVIA", "remplazar": "ADUANA NACIONAL"},
    {"busqueda": "ADUNA NACIONAL", "remplazar": "ADUANA NACIONAL"},
    {"busqueda": "S/I", "remplazar": ""},
]

# Mapeos para la limpieza del campo 'ubicacion'
UBICACION_MAPPINGS = [
    {"busqueda": "ALMACEN NRO 1", "remplazar": "ALMACÉN"},
    {"busqueda": "ALMACEN", "remplazar": "ALMACÉN"},
    {"busqueda": "ALMACÉN IMPORTACION", "remplazar": "ALMACÉN"},
    {"busqueda": "ALMACÉN IMPORTACION", "remplazar": "ALMACÉN"},

    {"busqueda": "ARCHIVO", "remplazar": "ARCHIVO AREA IMPORTACIONES ARCHIVO PLANTA ALTA"},

    {"busqueda": "ADUANA BOLIVIANA", "remplazar": "ADUANA BOLIVIA"},

    {"busqueda": "ALA DE ESPERA", "remplazar": "SALA DE ESPERA"},

    {"busqueda": "SPCC OFICINA SEGUNDO PISO", "remplazar": "SPCC"},
    {"busqueda": "SIN CLASIFICAR", "remplazar": "SIN UBICACIÓN"},

    {"busqueda": "AREA CUMUNES PRIMER PISO", "remplazar": "AREA COMUNES PRIMER PISO"},

    {"busqueda": "OF ADUANA BOLIVIA", "remplazar": "ADUANA BOLIVIA"},
    {"busqueda": "OFICINA ADUANA BOLIVIA", "remplazar": "ADUANA BOLIVIA"},
    {"busqueda": "OFICINAS ADUANA NACIONAL BOLIVIA", "remplazar": "ADUANA BOLIVIA"},

    {"busqueda": "OFICINAS ADUANA NACIONAL DE BOLIVIA", "remplazar": "ADUANA BOLIVIA"},
    {"busqueda": "OFICINAS ADUANA NACIONAL DE BOLIVIA VENTANILLA 2", "remplazar": "ADUANA BOLIVIA"},
    {"busqueda": "OFICINAS ADUANA NACIONAL VENTANILLA 2", "remplazar": "ADUANA BOLIVIA"},

    {"busqueda": "OFI ADUANA NACIONAL", "remplazar": "ADUANA BOLIVIA"},
    {"busqueda": "OFICINA ADUANA BOLIVIA", "remplazar": "ADUANA BOLIVIA"},
    {"busqueda": "OFICINA ADUANA IMPORTACION", "remplazar": "ADUANA BOLIVIA"},


    {"busqueda": "OF. MENOR CUANTIA", "remplazar": "MENOR CUANTIA"},
    {"busqueda": "OFICINAS MENOR CUANTIA", "remplazar": "MENOR CUANTIA"},

    {"busqueda": "ENFERMERIA IMPORTACIONES", "remplazar": "ENFERMERIA"},
    {"busqueda": "MONITOREO PLANTA BAJA", "remplazar": "CENTRO DE DATOS"},
    {"busqueda": "SALA DE COMPUTO", "remplazar": "CENTRO DE DATOS"},

    {"busqueda": "VENTANILLA UNICA", "remplazar": "VENTANILLA"},
    {"busqueda": "VENTANILLA 4 ATENCION A SIVETURS", "remplazar": "VENTANILLA"},
    {"busqueda": "VENTANILLA 1 ATENCION A CAMIONES Y/O CISTERNAS OFICINA ADUANA NACIONAL BOLIVIA", "remplazar": "VENTANILLA"},
    {"busqueda": "VENTANILLA 1", "remplazar": "VENTANILLA"},
    {"busqueda": "VENTANILLAS", "remplazar": "VENTANILLA"},
    {"busqueda": "ATENCION EN VENTANILLA", "remplazar": "VENTANILLA"},
    
    {"busqueda": "OFICINA SISTEMAS", "remplazar": "SISTEMAS"},
    {"busqueda": "OFICINA LICEN TABI", "remplazar": "SISTEMAS"},
    {"busqueda": "OF. SOPORTE SISTEMAS", "remplazar": "SISTEMAS"},
    {"busqueda": "OFICINAS SISTEMAS", "remplazar": "SISTEMAS"},

    {"busqueda": "OFICINA ADMINISTRACIÓN", "remplazar": "OFICINA ADMINISTRACION"},

    {"busqueda": "OFICINA ADUANA PARAGUAY", "remplazar": "ADUANA PARAGUAY"},

    {"busqueda": "OFICINA ALMACEN DE MATERIALES", "remplazar": "ALMACÉN"},

]

# Mapeos para la limpieza del campo 'area'
AREA_MAPPINGS = [
    {"busqueda": None, "remplazar": "SIN AREA"},
    {"busqueda": "IMPORTACIONES", "remplazar": "IMPORTACIÓN"},
    {"busqueda": "IMORTACIONES", "remplazar": "IMPORTACIÓN"},
    {"busqueda": "RECINTO DEPOSITO ADUANERO BOLIVIA DAB-CAÑADA ORURO", "remplazar": "IMPORTACIÓN"},

    {"busqueda": "EXPORTACIONES", "remplazar": "EXPORTACIÓN"},
    {"busqueda": "EXPORTACION", "remplazar": "EXPORTACIÓN"},

    {"busqueda": "VIVENDAS", "remplazar": "VIVIENDA"},
    {"busqueda": "VIVIENDA PARAGUAYA", "remplazar": "VIVIENDA"},
    {"busqueda": "VIVIENDAS", "remplazar": "VIVIENDA"},
    {"busqueda": "PARAGUAY", "remplazar": "VIVIENDA"},
]


