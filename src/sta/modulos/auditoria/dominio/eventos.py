from __future__ import annotations
from dataclasses import dataclass, field
from sta.seedwork.dominio.eventos import (EventoDominio)
import sta.modulos.auditoria.dominio.objetos_valor as ov
from datetime import datetime

class EventoRegulacion(EventoDominio):
    ...

@dataclass
class RegulacionCreada(EventoRegulacion):
    id_regulacion: uuid.UUID = None
    nombre: str = None
    version: str = None
    region: str = None
    requisitos: list[ov.Requisito] = field(default_factory=list[ov.Requisito])
    fecha_creacion: datetime = None