import pulsar
from pulsar.schema import *

from aeroalpes.modulos.auditoria.infraestructura.schema.v1.eventos import EventoRegulacionCreada
from aeroalpes.modulos.auditoria.infraestructura.schema.v1.comandos import ComandoCrearRegulacion, ComandoCrearRegulacionPayload
from aeroalpes.seedwork.infraestructura import utils

from aeroalpes.modulos.auditoria.infraestructura.mapeadores import MapadeadorEventosRegulacion

class Despachador:
    def __init__(self):
        self.mapper = MapadeadorEventosRegulacion()

    def _publicar_mensaje(self, mensaje, topico, schema):
        print("   ")
        print(f"==========PUBLICAR MENSAJE EN TOPICO PULSAR REGULACION============ {topico}")
        print(f"=====================MENSAJE============ {mensaje}")
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoRegulacionCreada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        print("   ")
        print(f"==========PUBLICAR EVENTO EN TOPICO ============{topico}")
        evento = self.mapper.entidad_a_dto(evento)
        self._publicar_mensaje(evento, topico, AvroSchema(evento.__class__))

    def publicar_comando(self, comando, topico):
        print("   ")
        print(F"==========PUBLICAR COMANDO EN TOPICO ============ {topico}")
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearRegulacionPayload(
            id_usuario=str(comando.id_usuario)
            # agregar itinerarios
        )
        comando_integracion = ComandoCrearRegulacion(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearRegulacion))
