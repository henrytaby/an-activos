from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Activo:
    nro: int
    codigo_anterior: Optional[str] = None
    codigo_nuevo: Optional[str] = None
    nro_acta: Optional[str] = None
    grupo: Optional[str] = None
    descripcion: Optional[str] = None
    serie: Optional[str] = None
    estado_uso_activo: Optional[str] = None
    estado_activo: bool = False
    area: Optional[str] = None
    ubicacion: Optional[str] = None
    asignado_a: Optional[str] = None
    observacion: Optional[str] = None
    saf: bool = False
    verificado_fisicamente: bool = False
    dar_baja: bool = False
    institucion: Optional[str] = None
    archivo: Optional[str] = None
    encargado: Optional[str] = None
    fecha_registro: Optional[str] = None
