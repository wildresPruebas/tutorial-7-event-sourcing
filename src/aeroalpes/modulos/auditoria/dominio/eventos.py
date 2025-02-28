from __future__ import annotations
from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoRegulacion(EventoDominio):
    ...

@dataclass
class RegulacionCreada(EventoRegulacion):
    id_regulacion: uuid.UUID = None
    nombre: str = None
    version: str = None
    region: str = None
    fecha_creacion: datetime = None