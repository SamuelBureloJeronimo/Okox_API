from database.db import Base
from sqlalchemy import Column, Integer, String, Text

class Motivo_Suspensiones(Base):
    __tablename__ = "motivo_suspensiones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)
    descripcion = Column(Text, nullable=False, default=0.0)

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f"ID(id={self.id}, nombre={self.nombre}, descripcion={self.descripcion})"

    def __str__(self):
        return f"Nombre de {self.nombre} registrada para el descripcion {self.descripcion}"