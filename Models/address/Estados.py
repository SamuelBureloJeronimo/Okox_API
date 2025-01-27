from database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Estados(Base):
    __tablename__ = "estados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    pais = Column(Integer, ForeignKey('paises.id'), nullable=True)  # Relación a una tabla de "Pais"
    
    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Paises = relationship("Paises", backref="estados")

    def __init__(self, nombre, pais=None):
        self.nombre = nombre
        self.pais = pais

    def __repr__(self):
        return f"Estado(id={self.id}, nombre={self.nombre}, pais={self.pais})"

    def __str__(self):
        return self.nombre
