from database.db import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class Clientes(Base):
    __tablename__ = "clientes"

    rfc = Column(String(13), ForeignKey('personas.rfc'), primary_key=True, unique=True)
    estado_servicio = Column(Integer, default=0)  # 0 == Activo, 1 == Suspendido
    fecha_contratacion = Column(DateTime, nullable=False)  # Fecha de contratación del servicio

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Personas = relationship("Personas", backref="clientes")

    def __init__(self, estado_servicio=0, fecha_contratacion=None):
        self.estado_servicio = estado_servicio
        self.fecha_contratacion = fecha_contratacion

    def __repr__(self):
        return f"Cliente(rfc={self.rfc}, " \
               f"estado_servicio={self.estado_servicio}, fecha_contratacion={self.fecha_contratacion})"

    def __str__(self):
        return f"Cliente ID {self.rfc} - Estado: {'Activo' if self.estado_servicio == 0 else 'Suspendido'}"
