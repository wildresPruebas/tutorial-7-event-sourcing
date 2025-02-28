import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from aeroalpes.modulos.auditoria.infraestructura.schema.v1.eventos import EventoRegulacionCreada
from aeroalpes.modulos.auditoria.infraestructura.schema.v1.comandos import ComandoCrearRegulacion


from aeroalpes.modulos.auditoria.infraestructura.proyecciones import ProyeccionRegulacionesLista
from aeroalpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from aeroalpes.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE PULSAR AL INICAR LA APP REGULACIONES")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-regulacion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoRegulacionCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR REGULacion: {datos}')
            print(f'requisitos: {datos.requisitos[0]}')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionRegulacionesLista(datos.id_regulacion, datos.nombre, datos.region, datos.version, datos.fecha_creacion, 
                                                            datos.requisitos, datos.fecha_creacion), app=app)
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!#1')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-regulacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearRegulacion))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos en Regulacion Consumidor!')
        traceback.print_exc()
        if cliente:
            cliente.close()