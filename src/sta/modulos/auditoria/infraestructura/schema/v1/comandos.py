from pulsar.schema import *
from dataclasses import dataclass, field
from sta.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearRegulacionPayload(ComandoIntegracion):
    id_usuario = String()
    # TODO Cree los records para itinerarios

class ComandoCrearRegulacion(ComandoIntegracion):
    data = ComandoCrearRegulacionPayload()