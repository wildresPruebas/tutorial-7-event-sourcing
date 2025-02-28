from sta.seedwork.aplicacion.queries import Query, QueryResultado
from sta.seedwork.aplicacion.queries import ejecutar_query as query
from sta.modulos.auditoria.dominio.entidades import Regulacion
from dataclasses import dataclass
from .base import RegulacionQueryBaseHandler
from sta.modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacion

@dataclass
class ObtenerRegulacion(Query):
    id: str

class ObtenerRegulacionHandler(RegulacionQueryBaseHandler):

    def handle(self, query: ObtenerRegulacion) -> QueryResultado:
        print("==========PASO#1============")
        vista = self.fabrica_vista.crear_objeto(Regulacion)
        print("==========PASO#2============")        
        result = vista.obtener_por(id=query.id)
        print("==========PASO#3============")
        reserva =  self.fabrica_auditorias.crear_objeto(result, MapeadorRegulacion())
        return QueryResultado(resultado=reserva)

@query.register(ObtenerRegulacion)
def ejecutar_query_obtener_reserva(query: ObtenerRegulacion):
    handler = ObtenerRegulacionHandler()
    return handler.handle(query)