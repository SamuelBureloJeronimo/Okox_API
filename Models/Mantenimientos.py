from database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Mantenimientos(Base):
    __tablename__ = "mantenimientos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(80), nullable=False)  # Descripción del mantenimiento
    descripcion = Column(String(200), nullable=False)  # Descripción del motivo del aviso
    fecha = Column(DateTime, nullable=False)  # Fecha y hora del mantenimiento
    colonia_afectada = Column(Integer, ForeignKey('colonias.id'), nullable=False)  # Relación a una colonia (posiblemente otra tabla)

    Colonias = relationship("Colonias", backref="mantenimientos")

    def __init__(self, titulo, descripcion, fecha=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha

    def __repr__(self):
        return f"Mantenimiento(id={self.id}, titulo={self.titulo}, " \
               f"fecha={self.fecha})"

    def __str__(self):
        return f"Mantenimiento programado el {self.fecha}"
