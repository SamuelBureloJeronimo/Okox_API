from database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Municipios(Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Integer, ForeignKey('estados.id'), nullable=True)  # Relación a una tabla de "Estados" si es necesario

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Estados = relationship("Estados", backref="municipios")

    def __init__(self, nombre, estado=None):
        self.nombre = nombre
        self.estado = estado

    def __repr__(self):
        return f"Municipio(id={self.id}, nombre={self.nombre}, estado={self.estado})"

    def __str__(self):
        return self.nombre
