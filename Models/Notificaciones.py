from database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Notificaciones(Base):
    __tablename__ = "notificaciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rfc = Column(String(13), ForeignKey('clientes.rfc')) # Relación con el Administrador que crea el aviso
    asunto = Column(String(80), nullable=False)  # Descripción del motivo del aviso
    descripcion = Column(String(200), nullable=False)  # Descripción del motivo del aviso
    tipo = Column(String(80), nullable=False)  # Descripción del motivo del aviso
    fecha_envio = Column(String(80), nullable=False)  # Descripción del motivo del aviso

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Clientes = relationship("Clientes", backref="notificaciones")

    def __init__(self, rfc, asunto, descripcion, tipo, fecha_envio):
        self.rfc = rfc
        self.asunto = asunto
        self.descripcion = descripcion
        self.tipo = tipo
        self.fecha_envio = fecha_envio

    def __repr__(self):
        return f"Notificaciones(id={self.id}, rfc={self.rfc}, " \
               f"asunto={self.asunto}, descripcion={self.descripcion})"

    def __str__(self):
        return f"Notificaciones: {self.rfc} Asunto {self.asunto} descripcion {self.descripcion}"
