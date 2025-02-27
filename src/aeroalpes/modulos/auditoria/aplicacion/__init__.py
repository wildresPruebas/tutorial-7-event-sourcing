from pydispatch import dispatcher

from .handlers import HandlerRegulacionIntegracion

from aeroalpes.modulos.auditoria.dominio.eventos import RegulacionCreada

dispatcher.connect(HandlerRegulacionIntegracion.handle_regulacion_creada, signal=f'{RegulacionCreada.__name__}Integracion')