from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class SafActivo:
    codigo: str
    grupo: Optional[str] = None
    descripcion: Optional[str] = None
    estado_uso_activo: Optional[str] = None
    responsable: Optional[str] = None
    fecha_registro: Optional[datetime] = None
