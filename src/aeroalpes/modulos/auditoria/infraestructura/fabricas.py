""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.repositorios import Repositorio
from aeroalpes.seedwork.infraestructura.vistas import Vista
from aeroalpes.modulos.auditoria.dominio.repositorios import RepositorioRegulaciones, RepositorioEventosRegulaciones
from .repositorios import RepositorioRegulacionesSQLAlchemy, RepositorioEventosRegulacionSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        print("                      RETORNA UN REPOSITORIO DE TIPO SQLAlchemy   ============")
        if obj == RepositorioRegulaciones:
            return RepositorioRegulacionesSQLAlchemy()
        elif obj == RepositorioEventosRegulaciones:            
            return RepositorioEventosRegulacionSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')