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
    nombre: ov.Nombre = field(default=ov.Nombre)
    nombre: ov.Nombre = field(default=ov.Nombre)
    region: ov.Region = field(default=ov.Region)
    version: ov.Version = field(default=ov.Version)
    requisitos: list[ov.Requisito] = field(default_factory=list[ov.Requisito])

    def crear_regulacion(self, regulacion: Regulacion):        
        self.nombre = regulacion.nombre
        self.region = regulacion.region
        self.version = regulacion.version
        self.requisitos = regulacion.requisitos
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(RegulacionCreada(id_regulacion=self.id, nombre=self.nombre, region=self.region, version = self.version,
                                              requisitos=self.requisitos, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación
