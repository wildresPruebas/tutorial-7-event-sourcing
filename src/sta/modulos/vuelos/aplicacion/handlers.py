from sta.modulos.vuelos.dominio.eventos import ReservaCreada, ReservaCancelada, ReservaAprobada, ReservaPagada
from sta.seedwork.aplicacion.handlers import Handler
from sta.modulos.vuelos.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_reserva_creada(evento):
        print("     ")
        print("==========INDICAR QUE LA RESERVA FUE CREADA ============")
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_reserva_cancelada(evento):
        print("     ")
        print("==========INDICAR QUE LA RESERVA FUE CANCELADA ============")
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_reserva_aprobada(evento):
        print("     ")
        print("==========INDICAR QUE LA RESERVA FUE APROBADA ============")
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_reserva_pagada(evento):
        print("     ")
        print("==========INDICAR QUE LA RESERVA FUE PAGADA ============")
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')


    