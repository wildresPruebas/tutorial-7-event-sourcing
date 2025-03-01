from sta.modulos.auditoria.dominio.entidades import Regulacion
from sta.config.db import db
from sta.modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacion
from .dto import Regulacion as RegulacionDTO
from sta.seedwork.infraestructura.vistas import Vista


class VistaRegulacion(Vista):
    def obtener_por(self,**kwargs) -> [Regulacion]:        
        params = {k: str(v) for k, v in kwargs.items() if v is not None}    
        map_regulacion = MapeadorRegulacion()
        regulacion_dto = db.session.query(RegulacionDTO).filter_by(**params).first()        
        if not regulacion_dto:
          return None 
        return map_regulacion.dto_a_entidad(regulacion_dto)
    
    def obtener_todas(self) -> [Regulacion]:
        map_regulacion = MapeadorRegulacion()
        regulaciones_dto = db.session.query(RegulacionDTO).all()    
        return map_regulacion.dto_a_entidad(regulaciones_dto)
