from database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Colonias(Base):
    __tablename__ = "colonias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    municipio = Column(Integer, ForeignKey('municipios.id'), nullable=True)  # Relación a una tabla de "Municipio"
    asentamiento = Column(String(100), nullable=True)
    codigo_postal = Column(Integer, nullable=True)

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Municipios = relationship("Municipios", backref="colonias")
    reportes_fugas = relationship("Reportes_Fugas", back_populates="Colonias")

    def __init__(self, nombre, ciudad, municipio=None, asentamiento=None, codigo_postal=None):
        self.nombre = nombre
        self.ciudad = ciudad
        self.municipio = municipio
        self.asentamiento = asentamiento
        self.codigo_postal = codigo_postal

    def __repr__(self):
        return f"Colonia(id={self.id}, nombre={self.nombre}, ciudad={self.ciudad}, " \
               f"municipio={self.municipio}, asentamiento={self.asentamiento}, codigo_postal={self.codigo_postal})"

    def __str__(self):
        return f"{self.nombre}, {self.ciudad}"
