from sta.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from sta.seedwork.aplicacion.queries import ejecutar_query as query
from sta.modulos.vuelos.infraestructura.repositorios import RepositorioReservas
from sta.modulos.vuelos.dominio.entidades import Reserva
from dataclasses import dataclass
from .base import ReservaQueryBaseHandler
from sta.modulos.vuelos.aplicacion.mapeadores import MapeadorReserva
import uuid

@dataclass
class ObtenerReserva(Query):
    id: str

class ObtenerReservaHandler(ReservaQueryBaseHandler):

    def handle(self, query: ObtenerReserva) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Reserva)
        print(f"Resltado {vista.obtener_por(id=query.id)}")
        reserva =  self.fabrica_vuelos.crear_objeto(vista.obtener_por(id=query.id), MapeadorReserva())
        return QueryResultado(resultado=reserva)

@query.register(ObtenerReserva)
def ejecutar_query_obtener_reserva(query: ObtenerReserva):
    handler = ObtenerReservaHandler()
    return handler.handle(query)