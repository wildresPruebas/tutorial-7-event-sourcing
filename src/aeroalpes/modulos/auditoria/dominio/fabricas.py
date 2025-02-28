""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Regulacion
from .reglas import MinimoUnRequisito
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from aeroalpes.seedwork.dominio.repositorios import Mapeador
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.entidades import Entidad
from aeroalpes.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaRegulacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            regulacion: Regulacion = mapeador.dto_a_entidad(obj)
            self.validar_regla(MinimoUnRequisito(regulacion.requisitos))            
            return regulacion

@dataclass
class FabricaAuditorias(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Regulacion.__class__:
            fabrica_regulacion = _FabricaRegulacion()
            return fabrica_regulacion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()

