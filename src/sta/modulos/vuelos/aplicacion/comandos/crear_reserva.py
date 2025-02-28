from sta.seedwork.aplicacion.comandos import Comando
from sta.modulos.vuelos.aplicacion.dto import ItinerarioDTO, ReservaDTO
from .base import CrearReservaBaseHandler
from dataclasses import dataclass, field
from sta.seedwork.aplicacion.comandos import ejecutar_commando as comando

from sta.modulos.vuelos.dominio.entidades import Reserva
from sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from sta.modulos.vuelos.aplicacion.mapeadores import MapeadorReserva
from sta.modulos.vuelos.infraestructura.repositorios import RepositorioReservas, RepositorioEventosReservas

#UN CommanHandler se usa para ejecutar el comando en este caso CrearReserva es el comando y CrearReservaHandler es el handler quien ejecuta al comando
@dataclass
class CrearReserva(Comando): #ESTE ES EL COMANDO
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    itinerarios: list[ItinerarioDTO]


class CrearReservaHandler(CrearReservaBaseHandler): #ESTE ES EL HANDLER
    
    def handle(self, comando: CrearReserva): #ACA RECIBE EL COMANDO POR PARAMETRO
        print("   ==========PASO#2 EJEUCTAR COMANDO USANDO EL HANDLER============")
        reserva_dto = ReservaDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   itinerarios=comando.itinerarios)
        print("      ==========PASO#3 CREAR============")
        reserva: Reserva = self.fabrica_vuelos.crear_objeto(reserva_dto, MapeadorReserva())
        print("      ==========PASO#5 CREAR RESERVA Y GUARDAR EL EVENTO============")
        reserva.crear_reserva(reserva)
        print("      ==========PASO#6 CREAR REPOSITORIO PARA ALAMCENAR EN <<<BD>>>============")
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas)
        print("      ==========PASO#7 CREAR REPOSITORIO EVENTOS <<<PARA GENERAR EL EVENTO QUE LA RESERVA FUE CREEADA>>>============")
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosReservas)
        print("      ==========PASO#8 GUARDAR LA RESERVA EN AL UOW PARA QUE ESTE DISPONIBLE EN TODA LA TRANSACCION Y REVERTIRLA SI FALLA  ============")
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, reserva, repositorio_eventos_func=repositorio_eventos.agregar)
        print("      ==========PASO#9 REALIZAR COMMIT DE LO QUE SE GUARDO  ============")
        UnidadTrabajoPuerto.commit()


@comando.register(CrearReserva)
def ejecutar_comando_crear_reserva(comando: CrearReserva):
    print("     ")
    print("==========PASO#1 SOLICITAR EJEUCTAR COMANDO============")
    handler = CrearReservaHandler()
    handler.handle(comando)
    