from database.db import Base
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Reportes_Fugas(Base):
    __tablename__ = "reportes_fugas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rfc = Column(String(13), ForeignKey('clientes.rfc'), nullable=False)
    foto = Column(LargeBinary(length=16777215), nullable=False)
    mensaje = Column(String(500), nullable=False)  # Mensaje con un límite razonable de longitud
    atendido = Column(Boolean, default=False, nullable=False)
    id_colonia = Column(Integer, ForeignKey('colonias.id'), nullable=False)  # Relación a una colonia (posiblemente otra tabla)

    Colonias = relationship("Colonias", back_populates="reportes_fugas")
    Clientes = relationship("Clientes", backref="reportes_fugas");

    def __init__(self, rfc, foto, mensaje, atendido=False, id_colonia=None):
        self.rfc = rfc
        self.foto = foto
        self.mensaje = mensaje
        self.atendido = atendido
        self.id_colonia = id_colonia

    def __repr__(self):
        return f"Reporte(cliente={self.rfc}, mensaje={self.mensaje[:50]}...)"

    def __str__(self):
        return f"Reporte del cliente {self.rfc}: {self.mensaje[:50]}..."
