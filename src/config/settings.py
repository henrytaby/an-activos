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
    {"busqueda": "IMPRESORA A LASER", "remplazar": "IMPRESORA"},
    {"busqueda": "MEZON DE METAL", "remplazar": "MESON"},
    {"busqueda": "GABETERO", "remplazar": "GAVETERO"},
    {"busqueda": "UPS TRIPP-LITE", "remplazar": "UPS"},
    {"busqueda": "TELEVISOR LED", "remplazar": "TELEVISOR"},
    {"busqueda": "SILLA GIRATORIA EN TAPIZ", "remplazar": "SILLA"},
    {"busqueda": "APARATO TELÉFONO", "remplazar": "TELEFONO"},
    {"busqueda": "RELOJ BIOMETRICO", "remplazar": "EQUIPO BIOMETRICO"},
    {"busqueda": "TELÉFONO", "remplazar": "TELEFONO"},
    
    
     
]