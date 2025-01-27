from database.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship


class Personas(Base):
    __tablename__ = "personas"

    rfc = Column(String(13), primary_key=True)
    nombre = Column(String(100), nullable=False)
    app = Column(String(100), nullable=False)  # Apellido paterno
    apm = Column(String(100), nullable=False)  # Apellido materno
    fech_nac = Column(Date, nullable=False)  # Fecha de nacimiento
    sex = Column(String(1), nullable=False)  # Género ('M' o 'F')
    id_colonia = Column(Integer, ForeignKey('colonias.id'), nullable=False)  # Relación a una colonia (posiblemente otra tabla)

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Colonias = relationship("Colonias", backref="personas")

    def __init__(self, nombre, app, apm=None, fech_nac=None, sex="", id_colonia=None):
        self.nombre = nombre
        self.app = app
        self.apm = apm
        self.fech_nac = fech_nac
        self.sex = sex
        self.id_colonia = id_colonia

    def __repr__(self):
        return (
            f"Persona(rfc={self.rfc}, nombre={self.nombre}, app={self.app}, "
            f"apm={self.apm}, fech_nac={self.fech_nac}, sex={self.sex})"
        )

    def __str__(self):
        return f"{self.nombre} {self.app} {self.apm or ''}".strip()
