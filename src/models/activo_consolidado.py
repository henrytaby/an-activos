from typing import Optional, List
from datetime import datetime

class ActivoConsolidado:
    def __init__(
        self,
        codigo_anterior: Optional[str] = None,
        codigo_nuevo: Optional[str] = None,
        nroacta: Optional[str] = None,
        grupo: Optional[str] = None,
        descripcion: Optional[str] = None,
        serie: Optional[str] = None,
        estado_uso_activo: Optional[str] = None,
        area: Optional[str] = None,
        ubicacion: Optional[str] = None,
        asignado_a: Optional[str] = None,
        observacion: Optional[str] = None,
        saf: bool = False,
        verificado_fisicamente: bool = False,
        dar_baja: bool = False,
        institucion: Optional[str] = None,
        fecha_registro: datetime = datetime.now(),
        encargado: Optional[str] = None,
        archivo: Optional[str] = None,
    ):
        self.codigo_anterior = codigo_anterior
        self.codigo_nuevo = codigo_nuevo
        self.nroacta = nroacta
        self.grupo = grupo
        self.descripcion = descripcion
        self.serie = serie
        self.estado_uso_activo = estado_uso_activo
        self.area = area
        self.ubicacion = ubicacion
        self.asignado_a = asignado_a
        self.observacion = observacion
        self.saf = saf
        self.verificado_fisicamente = verificado_fisicamente
        self.dar_baja = dar_baja
        self.institucion = institucion
        self.fecha_registro = fecha_registro
        self.encargado = encargado
        self.archivo = archivo

    def to_dict(self):
        return self.__dict__
