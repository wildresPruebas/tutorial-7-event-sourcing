# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import vuelos_pb2 as vuelos__pb2


class VuelosStub(object):
    """------------------------------
    Servicios
    ------------------------------

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CrearReserva = channel.unary_unary(
                '/vuelos.Vuelos/CrearReserva',
                request_serializer=vuelos__pb2.Reserva.SerializeToString,
                response_deserializer=vuelos__pb2.RespuestaReserva.FromString,
                )
        self.ConsultarReserva = channel.unary_unary(
                '/vuelos.Vuelos/ConsultarReserva',
                request_serializer=vuelos__pb2.QueryReserva.SerializeToString,
                response_deserializer=vuelos__pb2.RespuestaReserva.FromString,
                )


class VuelosServicer(object):
    """------------------------------
    Servicios
    ------------------------------

    """

    def CrearReserva(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConsultarReserva(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VuelosServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CrearReserva': grpc.unary_unary_rpc_method_handler(
                    servicer.CrearReserva,
                    request_deserializer=vuelos__pb2.Reserva.FromString,
                    response_serializer=vuelos__pb2.RespuestaReserva.SerializeToString,
            ),
            'ConsultarReserva': grpc.unary_unary_rpc_method_handler(
                    servicer.ConsultarReserva,
                    request_deserializer=vuelos__pb2.QueryReserva.FromString,
                    response_serializer=vuelos__pb2.RespuestaReserva.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'vuelos.Vuelos', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Vuelos(object):
    """------------------------------
    Servicios
    ------------------------------

    """

    @staticmethod
    def CrearReserva(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/vuelos.Vuelos/CrearReserva',
            vuelos__pb2.Reserva.SerializeToString,
            vuelos__pb2.RespuestaReserva.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConsultarReserva(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/vuelos.Vuelos/ConsultarReserva',
            vuelos__pb2.QueryReserva.SerializeToString,
            vuelos__pb2.RespuestaReserva.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
