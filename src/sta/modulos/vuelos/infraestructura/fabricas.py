""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from sta.seedwork.dominio.fabricas import Fabrica
from sta.seedwork.dominio.repositorios import Repositorio
from sta.seedwork.infraestructura.vistas import Vista
from sta.modulos.vuelos.infraestructura.vistas import VistaReserva
from sta.modulos.vuelos.dominio.entidades import Reserva
from sta.modulos.vuelos.dominio.repositorios import RepositorioProveedores, RepositorioReservas, RepositorioEventosReservas
from .repositorios import RepositorioReservasSQLAlchemy, RepositorioProveedoresSQLAlchemy, RepositorioEventosReservaSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        print("                      RETORNA UN REPOSITORIO DE TIPO SQLAlchemy   ============")
        if obj == RepositorioReservas:
            return RepositorioReservasSQLAlchemy()
        elif obj == RepositorioProveedores:
            return RepositorioProveedoresSQLAlchemy()
        elif obj == RepositorioEventosReservas:            
            return RepositorioEventosReservaSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')

@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        print("Entra1.1")
        if obj == Reserva:
            print("Entra1.2")
            return VistaReserva()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')