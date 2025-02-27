from aeroalpes.seedwork.aplicacion.dto import Mapeador as AppMap
from aeroalpes.seedwork.dominio.repositorios import Mapeador as RepMap
from aeroalpes.modulos.auditoria.dominio.entidades import Regulacion
from aeroalpes.modulos.auditoria.dominio.objetos_valor import Requisito
from .dto import RegulacionDTO, RequisitoDTO

class MapeadorRegulacionDTOJson(AppMap):
    def _procesar_requisito(self, requisito: dict) -> RequisitoDTO:
        return RequisitoDTO(requisito.get('codigo'), requisito.get('descripcion'), requisito.get('obligatorio'))
    
    def externo_a_dto(self, externo: dict) -> RegulacionDTO:
        regulacion_dto = RegulacionDTO()
        for req in externo.get('requisitos', list()):
            regulacion_dto.requisitos.append(self._procesar_requisito(req))

        return regulacion_dto

    def dto_a_externo(self, dto: RegulacionDTO) -> dict:
        return dto.__dict__

class MapeadorRegulacion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_requisito(self, requsito_dto: RequisitoDTO) -> Requisito:
        return Requisito(requsito_dto.codigo, requsito_dto.descripcion, requsito_dto.obligatorio)

    def obtener_tipo(self) -> type:
        return Regulacion.__class__

    def locacion_a_dict(self, locacion):
        if not locacion:
            return dict(codigo=None, descripcion=None, obligatorio=None, fecha_actualizacion=None, fecha_creacion=None)
        
        return dict(
                    codigo=locacion.codigo,
                    descripcion=locacion.descripcion,
                    obligatorio=locacion.obligatorio,
                    fecha_actualizacion=locacion.fecha_actualizacion.strftime(self._FORMATO_FECHA),
                    fecha_creacion=locacion.fecha_creacion.strftime(self._FORMATO_FECHA)
        )
        

    def entidad_a_dto(self, entidad: Regulacion) -> RegulacionDTO:
        
        _id = str(entidad.id)
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)        
        requisitos = list()

        for req in entidad.requisitos:
            requisitos.append(RequisitoDTO(codigo=req.codigo, descripcion=req.descripcion, obligatorio=req.obligatorio))
        
        return RegulacionDTO(fecha_creacion, fecha_actualizacion, _id, requisitos)

    def dto_a_entidad(self, dto: RegulacionDTO) -> Regulacion:
        regulacion = Regulacion()
        regulacion.requisitos = list()

        requisitos_dto: list[RequisitoDTO] = dto.requisitos

        for req in requisitos_dto:
            regulacion.requisitos.append(self._procesar_requisito(req))
        
        return regulacion



