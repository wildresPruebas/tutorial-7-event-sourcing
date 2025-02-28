from sta.seedwork.aplicacion.queries import Query, QueryResultado
from sta.seedwork.aplicacion.queries import ejecutar_query as query
from sta.modulos.auditoria.dominio.entidades import Regulacion
from dataclasses import dataclass
from .base import RegulacionQueryBaseHandler
from sta.modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacion

@dataclass
class ObtenerTodasRegulacion(Query):
    pass

class ObtenerTodasRegulacionHandler(RegulacionQueryBaseHandler):

    def handle(self, query: ObtenerTodasRegulacion) -> QueryResultado:        
        vista = self.fabrica_vista.crear_objeto(Regulacion)          
        result = vista.obtener_todas()        
        regulacion =  self.fabrica_auditorias.crear_objeto(result, MapeadorRegulacion())
        return QueryResultado(resultado=regulacion)

@query.register(ObtenerTodasRegulacion)
def ejecutar_query_obtener_reservas(query: ObtenerTodasRegulacion):
    handler = ObtenerTodasRegulacionHandler()
    return handler.handle(query)