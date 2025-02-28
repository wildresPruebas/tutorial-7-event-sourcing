"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from sta.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey

import uuid

Base = db.declarative_base()

class Regulacion(db.Model):
    __tablename__ = "regulaciones"
    id = db.Column(db.String(40), primary_key=True)
    nombre = db.Column(db.String(500), nullable=False)
    region = db.Column(db.String(500), nullable=False)
    version = db.Column(db.String(500), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    requisitos = relationship("Requisito", back_populates="regulacion", cascade="all, delete-orphan")    

class Requisito(db.Model):
    __tablename__ = "requisitos"
     
    id = db.Column(db.String(40), primary_key=True, default=uuid.uuid4) 
    codigo = Column(db.String(10), nullable=False)
    descripcion = Column(db.String(500), nullable=False)
    obligatorio = Column(db.Boolean, nullable=False)
    regulacion_id = Column(db.String(40), ForeignKey("regulaciones.id"), nullable=False)

    regulacion = relationship("Regulacion", back_populates="requisitos")

class EventosRegulacion(db.Model):
    __tablename__ = "eventos_regulacion"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)