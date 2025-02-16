from database.db import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship


class Clientes(Base):
    __tablename__ = "clientes"

    rfc = Column(String(13), ForeignKey('personas.rfc'), primary_key=True, unique=True)  
    id_umbral = Column(Integer, ForeignKey('umbral_clientes.id'), default=0, nullable=False)
    id_company = Column(Integer, ForeignKey('company.id'), default=0, nullable=False)
    fecha_contratacion = Column(DateTime, default=func.now(), nullable=False)  # Fecha de contratación del servicio

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Personas = relationship("Personas", backref="clientes")
    Umbral_Clientes = relationship("Umbral_Clientes", backref="clientes")
    Company = relationship("Company", backref="clientes")

    def __init__(self, rfc, id_umbral, id_company, fecha_contratacion=None):
        self.rfc = rfc
        self.id_umbral = id_umbral
        self.id_company = id_company
        self.fecha_contratacion = fecha_contratacion

    def __repr__(self):
        return f"Cliente(rfc={self.rfc}, " \
               f"estado_servicio={self.estado_servicio}, fecha_contratacion={self.fecha_contratacion})"

    def __str__(self):
        return f"Cliente ID {self.rfc} - Estado: {'Activo' if self.estado_servicio == 0 else 'Suspendido'}"
