from sta.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from sta.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from sta.modulos.auditoria.infraestructura.fabricas import FabricaRepositorio
from sta.modulos.auditoria.infraestructura.repositorios import RepositorioRegulaciones
from sta.modulos.auditoria.dominio.entidades import Regulacion
from sta.modulos.auditoria.infraestructura.dto import Regulacion as RegulacionDTO

from sta.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod

class ProyeccionRegulacion(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionRegulacionesLista(ProyeccionRegulacion):
    print("ENTRA PROYECCION REGULACIONES")
    def __init__(self, id_regulacion, nombre, region, version, fecha_creacion, requisitos, fecha_actualizacion):
        self.id_regulacion = id_regulacion
        self.nombre = nombre
        self.region = region
        self.version = version     
        self.requisitos = requisitos
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.fecha_actualizacion = millis_a_datetime(fecha_actualizacion)
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioRegulaciones)
        print("aca es la proyeccion algo debe hacer Y PERSISTE ALGO, REVISAR")
        repositorio.agregar(
            Regulacion(
                id=str(self.id_regulacion), 
                nombre=str(self.nombre), 
                region=str(self.region), 
                version=str(self.version), 
                requisitos=self.requisitos,
                fecha_creacion=self.fecha_creacion, 
                fecha_actualizacion=self.fecha_actualizacion))
        db.session.commit()

class ProyeccionRegulacionHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionRegulacion):

        # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
        # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
        # podriamos diseñar para alojar esta funcionalidad
        from sta.config.db import db

        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionRegulacionesLista)
def ejecutar_proyeccion_regulacion(proyeccion, app=None):
    print("REGISTRAR PROYECCION REGULACIONES")
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionRegulacionHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    