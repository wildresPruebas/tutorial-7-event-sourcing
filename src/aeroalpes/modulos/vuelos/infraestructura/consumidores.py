import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from aeroalpes.modulos.auditoria.infraestructura.schema.v1.eventos import EventoRegulacionCreada
from aeroalpes.modulos.auditoria.infraestructura.schema.v1.comandos import ComandoCrearRegulacion


from aeroalpes.modulos.vuelos.infraestructura.proyecciones import ProyeccionReservasLista, ProyeccionReservasTotales
from aeroalpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from aeroalpes.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE PULSAR AL INICAR LA APP REGULACIONES")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-reserva', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoRegulacionCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR: {datos}')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionReservasTotales(datos.fecha_creacion, ProyeccionReservasTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionReservasLista(datos.id_reserva, datos.id_cliente, datos.estado, datos.fecha_creacion, datos.fecha_creacion), app=app)
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-reserva', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearRegulacion))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()