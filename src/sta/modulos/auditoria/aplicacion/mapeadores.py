from sta.seedwork.aplicacion.dto import Mapeador as AppMap
from sta.seedwork.dominio.repositorios import Mapeador as RepMap
from sta.modulos.auditoria.dominio.entidades import Regulacion
from sta.modulos.auditoria.dominio.objetos_valor import Requisito
from .dto import RegulacionDTO, RequisitoDTO

class MapeadorRegulacionDTOJson(AppMap):
    def _procesar_requisito(self, requisito: dict) -> RequisitoDTO:
        return RequisitoDTO(requisito.get('codigo'), requisito.get('descripcion'), requisito.get('obligatorio'))
    
    def externo_a_dto(self, externo: dict) -> RegulacionDTO:
        regulacion_dto = RegulacionDTO(externo.get('id'), externo.get('nombre'), externo.get('region'), externo.get('version'))    
        for req in externo.get('requisitos', list()):
            regulacion_dto.requisitos.append(self._procesar_requisito(req))

        return regulacion_dto

    def dto_a_externo(self, dto: RegulacionDTO) -> dict:
        if isinstance(dto, list):  # Si es una lista, convertir cada elemento
          return [self.dto_a_externo(item) for item in dto]
        else:   
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
        nombre= str(entidad.nombre)
        region= str(entidad.region)
        version= str(entidad.version)
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)        
        requisitos = list()

        for req in entidad.requisitos:
            requisitos.append(RequisitoDTO(codigo=req.codigo, descripcion=req.descripcion, obligatorio=req.obligatorio))
        
        return RegulacionDTO(_id, nombre, region, version, fecha_creacion, fecha_actualizacion, requisitos)

    def dto_a_entidad(self, dto: RegulacionDTO) -> Regulacion:

        if isinstance(dto, list): 
          return [self.dto_a_entidad(item) for item in dto]
        
        regulacion = Regulacion()
        regulacion.nombre = dto.nombre
        regulacion.region = dto.region
        regulacion.version = dto.version
        regulacion.requisitos = list()
        requisitos_dto: list[RequisitoDTO] = dto.requisitos

        for req in requisitos_dto:
            regulacion.requisitos.append(self._procesar_requisito(req))
        
        return regulacion



