from __future__ import annotations

from dataclasses import dataclass, field
from sta.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class Requisito(ObjetoValor):
    codigo: str
    descripcion: str
    obligatorio: bool

@dataclass(frozen=True)
class Nombre():
    nombre: str

@dataclass(frozen=True)
class Region():
    nombre: str

@dataclass(frozen=True)
class Version():
    nombre: str    