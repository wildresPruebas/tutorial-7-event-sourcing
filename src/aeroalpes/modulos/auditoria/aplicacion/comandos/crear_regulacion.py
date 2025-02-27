from aeroalpes.seedwork.aplicacion.comandos import Comando
from aeroalpes.modulos.auditoria.aplicacion.dto import RequisitoDTO, RegulacionDTO
from .base import CrearRegulacionBaseHandler
from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from aeroalpes.modulos.auditoria.dominio.entidades import Regulacion
from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from aeroalpes.modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacion
from aeroalpes.modulos.auditoria.infraestructura.repositorios import RepositorioRegulaciones, RepositorioEventosRegulaciones

#UN CommanHandler se usa para ejecutar el comando en este caso CrearReserva es el comando y CrearReservaHandler es el handler quien ejecuta al comando
@dataclass
class CrearRegulacion(Comando): #ESTE ES EL COMANDO
    id: str
    nombre: str
    region: str    
    version: str 
    fecha_actualizacion: str 
    requisitos: list[RequisitoDTO]


class CrearRegulacionHandler(CrearRegulacionBaseHandler): #ESTE ES EL HANDLER
    
    def handle(self, comando: CrearRegulacion): #ACA RECIBE EL COMANDO POR PARAMETRO

        regulacion_dto = RegulacionDTO(id=comando.id, nombre=comando.nombre, region=comando.region, version= comando.version, 
                                       fecha_actualizacion= comando.fecha_actualizacion, requisitos=comando.requisitos)
        
        regulacion: Regulacion = self.fabrica_auditorias.crear_objeto(regulacion_dto, MapeadorRegulacion())
        regulacion.crear_regulacion(regulacion)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioRegulaciones)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosRegulaciones)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, regulacion, repositorio_eventos_func=repositorio_eventos.agregar)        
        UnidadTrabajoPuerto.commit()


@comando.register(CrearRegulacion)
def ejecutar_comando_crear_regulacion(comando: CrearRegulacion):
    print("     ")
    print("==========PASO#1 SOLICITAR EJEUCTAR COMANDO============")
    handler = CrearRegulacionHandler()
    handler.handle(comando)
    