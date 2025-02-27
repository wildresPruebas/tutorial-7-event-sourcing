from aeroalpes.seedwork.aplicacion.handlers import Handler
from aeroalpes.modulos.auditoria.infraestructura.despachadores import Despachador

class HandlerRegulacionIntegracion(Handler):

    @staticmethod
    def handle_regulacion_creada(evento):
        print("     ")
        print("==========INDICAR QUE LA REGULACION FUE CREADA ============")
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-regulacion')


    