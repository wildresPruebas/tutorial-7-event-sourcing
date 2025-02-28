from sta.modulos.auditoria.dominio.entidades import Regulacion
from sta.config.db import db
from sta.modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacion
from .dto import Regulacion as RegulacionDTO
from sta.seedwork.infraestructura.vistas import Vista


class VistaRegulacion(Vista):
    def obtener_por(self,**kwargs) -> [Regulacion]:
        print("==========PASO#2.1============")   
        params = {k: str(v) for k, v in kwargs.items() if v is not None}
        print("==========PASO#2.2============")   
        map_regulacion = MapeadorRegulacion()
        print("==========PASO#2.3============")   
        regulacion_dto = db.session.query(RegulacionDTO).filter_by(**params).first()      
        print(f"==========PASO#2.4============ {regulacion_dto}")     
        return map_regulacion.dto_a_entidad(regulacion_dto)
