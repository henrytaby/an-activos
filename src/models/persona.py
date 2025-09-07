from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Persona:
    funcionarioId: int
    nombre: Optional[str] = None
    ci: Optional[str] = None
    ci_exp: Optional[str] = None
    celular: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    usuario: Optional[str] = None
    item: Optional[int] = None
    nivel: Optional[str] = None
    basico: Optional[float] = None
    email: Optional[str] = None
    recinto_electoral: Optional[str] = None
    mesa: Optional[str] = None
    departamento: Optional[str] = None
    localidad: Optional[str] = None
    saf_id: Optional[int] = None
    fecha_registro: Optional[datetime] = None
