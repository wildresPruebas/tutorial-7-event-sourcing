import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime
import io
import fastavro
import json

from sta.modulos.auditoria.infraestructura.schema.v1.eventos import EventoRegulacionCreada
from sta.modulos.auditoria.infraestructura.schema.v1.comandos import ComandoCrearRegulacion


from sta.modulos.auditoria.infraestructura.proyecciones import ProyeccionRegulacionesLista
from sta.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from sta.seedwork.infraestructura import utils


ADMIN_URL = f'http://{utils.broker_host()}:8080/admin/v2'
print(f"LA URL ESSSSSSSSSSS: {ADMIN_URL}")

def realizar_suscripcion(app=None):
    consumidores = {}
    client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')

    try:
        while True:
            print("🔍 BUSCANDO TÓPICOS CADA 10 SEGUNDOS...")
            try:
                topicos_actuales = set(obtener_topicos())
                print(f"   📡 TÓPICOS ENCONTRADOS: {topicos_actuales}")
            except Exception as e:
                logging.error(f"ERROR: No se pudieron obtener los tópicos - {e}")
                continue  # Evita que el bucle se detenga

            for topic in topicos_actuales:
                if topic not in consumidores:
                    print(f"USCRIBIENDO A TÓPICO {topic}")
                    try:
                        consumidores[topic] = consumir_topico(client, topic)
                    except Exception as e:
                        logging.error(f'ERROR: Suscribiéndose al tópico {topic} - {e}')
            
            time.sleep(5)  # ⏳ Espera 10 segundos antes de la próxima búsqueda
            
    except KeyboardInterrupt:
        print("Deteniendo suscripción...")
    
    finally:
        print("🔌 Cerrando cliente de Pulsar...")
        client.close()  # AHORA SE CIERRA CORRECTAMENTE



# Obtener lista de tópicos disponibles en el namespace
def obtener_topicos():
    NAMESPACE = "public/default"
    url = f"{ADMIN_URL}/persistent/{NAMESPACE}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        print(f"Error obteniendo tópicos: {response.text}")
    except requests.RequestException as e:
        print(f"Error de conexión con Pulsar Admin: {e}")
    return []


# Función para consumir mensajes de un tópico sin esquema
def consumir_topico(cliente, topic, app=None):
    print(f"SUSCRIBIENDOSE A TOPICO : {topic}")
    try:        
        nombre_topico = topic.split("/")[-1]
        print(f"SUSCRITO A TOPICO ARREGLADO: {nombre_topico}")
        consumidor = cliente.subscribe(nombre_topico, subscription_name="auto-suscripcion",   consumer_type=pulsar.ConsumerType.Shared)  
        print(f"SUSCRITO A TOPICO : {nombre_topico}")
        while True:
            print(f"Mensaje RECIBIDO EN BINARIO DINAMICO : {contenido}")
            mensaje = consumidor.receive()
            contenido = mensaje.data()  # Se recibe en formato binario (bytes)
            print(f"Mensaje recibido EN BINARIO DINAMICO : {contenido}")
            esquema_avro = obtener_esquema(topic)
            print(f"Se obtiene el esquema : {esquema_avro}")
            if esquema_avro:

                try:
                    with io.BytesIO(contenido) as bio:
                        evento = fastavro.schemaless_reader(bio, esquema_avro)  # Usa tu esquema AVRO aquí
                    print(f"Mensaje decodificado: {evento}")
                except Exception as e:
                    print(f"Error al decodificar AVRO: {e}")

                ##contenido_decodificado = decodificar_avro(contenido, esquema_avro)
                # print(f"Mensaje decodificado: {contenido_decodificado}")
                consumidor.acknowledge(mensaje)
        cliente.close()
    except Exception as e:
        print(f" Error inesperado: {e}")
        logging.error('ERROR: Suscribiendose al tópico de eventos TODOS ')
        traceback.print_exc()


def obtener_esquema(topic):
    topico_limpio = topic.replace("persistent://", "")
    url = f"{ADMIN_URL}/schemas/{topico_limpio}/schema"
    print(f"LA URL ES {url}")
    response = requests.get(url)
    print(f"LA RESPUESTA ES {response}")
    if response.status_code == 200:
        print(f"STARTUS ES : {response.status_code}")
        print(f"SE ENCONTRO SCHEMA: {response}")
        esquema_json = response.json().get("data")
        print(f"EL ESUQMEA ES: {esquema_json}")
        return json.loads(esquema_json)  # Retorna el esquema como diccionario
    return None


def decodificar_avro(mensaje_binario, esquema_avro):
    """Deserializa un mensaje AVRO binario usando su esquema."""
    with io.BytesIO(mensaje_binario) as bio:
        print(F"ACA PASA EL ERROR {mensaje_binario}")
        print(F"ACA PASA EL bio {bio}")
        reader = fastavro.reader(bio)
        return [record for record in reader]  # Retorna los datos deserializados


# DE ACA ES COMO ESTABA
def suscribirse_a_eventos(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE PULSAR AL INICAR LA APP REGULACIONES")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-regulacion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos', schema=AvroSchema(EventoRegulacionCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print('Evento recibido EN PULSAR REGULacion:')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionRegulacionesLista(datos.id_regulacion, datos.nombre, datos.region, datos.version, datos.fecha_creacion, 
                                                            datos.requisitos, datos.fecha_creacion), app=app)
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!#1')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-regulacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='sta-sub-comandos', schema=AvroSchema(ComandoCrearRegulacion))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos en Regulacion Consumidor!')
        traceback.print_exc()
        if cliente:
            cliente.close()
