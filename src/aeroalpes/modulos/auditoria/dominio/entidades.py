"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import aeroalpes.modulos.auditoria.dominio.objetos_valor as ov
from aeroalpes.modulos.auditoria.dominio.eventos import RegulacionCreada
from aeroalpes.seedwork.dominio.entidades import AgregacionRaiz

@dataclass
class Regulacion(AgregacionRaiz):
    requisitos: list[ov.Requisito] = field(default_factory=list[ov.Requisito])

    def crear_regulacion(self, regulacion: Regulacion):        
        self.requisitos = regulacion.requisitos
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(RegulacionCreada(id_regulacion=self.id, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación
