from database.db import Base
from sqlalchemy import Column, Integer, String


class Paises(Base):
    __tablename__ = "paises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Pais(id={self.id}, nombre={self.nombre})"

    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }
