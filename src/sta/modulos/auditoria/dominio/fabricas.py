""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Regulacion
from .reglas import MinimoUnRequisito
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from sta.seedwork.dominio.repositorios import Mapeador
from sta.seedwork.dominio.fabricas import Fabrica
from sta.seedwork.dominio.entidades import Entidad
from sta.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaRegulacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, list):
            return [self.crear_objeto(item, mapeador) for item in obj]
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
            print("ENTRA IF")
            fabrica_regulacion = _FabricaRegulacion()
            return fabrica_regulacion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()

