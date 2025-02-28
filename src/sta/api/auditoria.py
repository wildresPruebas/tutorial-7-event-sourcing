import sta.seedwork.presentacion.api as api
import json
from sta.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, session
from flask import Response
from sta.modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacionDTOJson
from sta.modulos.auditoria.aplicacion.comandos.crear_regulacion import CrearRegulacion
from sta.modulos.auditoria.aplicacion.queries.obtener_regulacion import ObtenerRegulacion
from sta.seedwork.aplicacion.comandos import ejecutar_commando
from sta.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('auditoria', '/auditoria')

@bp.route('/regulacion', methods=('POST',))
def regulacion_usando_comando():
    try:
        print("==========ENTRA ENDOPINT  CREAR REGULACION ============")
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'

        regulacion_dict = request.json

        map_regulacion = MapeadorRegulacionDTOJson()
        regulacion_dto = map_regulacion.externo_a_dto(regulacion_dict)
        print(f"json regulacion_dto es {regulacion_dto}")
        comando = CrearRegulacion(regulacion_dto.id,
                                  regulacion_dto.nombre, 
                                  regulacion_dto.region,
                                  regulacion_dto.version,
                                  regulacion_dto.fecha_actualizacion,
                                  regulacion_dto.requisitos)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura        
        print("PASO FINALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        ejecutar_commando(comando)
        print("==================TERMINA============================")
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    

@bp.route('/regulacion', methods=('GET',))
@bp.route('/regulacion/<id>', methods=('GET',))
def dar_regulacion_usando_query(id=None):
    if id:
        print("==========ENTRA ENDOPINT CONSULTAR REGULACION ============")
        query_resultado = ejecutar_query(ObtenerRegulacion(id))
        map_regulacion = MapeadorRegulacionDTOJson()
        
        return map_regulacion.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]