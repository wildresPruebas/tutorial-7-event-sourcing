from aeroalpes.seedwork.infraestructura.vistas import Vista
from aeroalpes.modulos.vuelos.dominio.entidades import Reserva
from aeroalpes.config.db import db
from .dto import Reserva as ReservaDTO
from aeroalpes.modulos.vuelos.aplicacion.mapeadores import MapeadorReserva

class VistaReserva(Vista):
    def obtener_por(self,**kwargs) -> [Reserva]:
        params = {k: str(v) for k, v in kwargs.items() if v is not None}
            
        # TODO Convierta ReservaDTO a Reserva y valide que la consulta es correcta        
        map_reserva = MapeadorReserva()
        rserva_dto = db.session.query(ReservaDTO).filter_by(**params).first()        
        return map_reserva.dto_a_entidad(rserva_dto)
