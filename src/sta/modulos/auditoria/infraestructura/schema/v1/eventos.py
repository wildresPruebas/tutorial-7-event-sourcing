from pulsar.schema import *
from sta.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from sta.seedwork.infraestructura.utils import time_millis
import uuid

class Requisito(Record):
    codigo = String()
    descripcion = String()
    obligatorio = Boolean()

class RegulacionCreadaPayload(Record):
    id_regulacion = String()
    nombre = String()
    region = String()
    version = String()
    requisitos = Array(Requisito())
    fecha_creacion = Long()       

class EventoRegulacionCreada(EventoIntegracion):
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados, 
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = RegulacionCreadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)