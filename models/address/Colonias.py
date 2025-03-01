from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Colonias(Base):
    __tablename__ = 'colonias'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    municipio = Column(Integer, ForeignKey('municipios.id'))
    asentamiento = Column(String(100))
    codigo_postal = Column(Integer)
    
    # ForaignKey propias de la clase
    municipios = relationship("Municipios", back_populates="fk_colonias")
    # ForaignKey que apuntan a esta clase <-
    fk_personas = relationship("Personas", back_populates="colonias")
    fk_companies = relationship("Companies", back_populates="colonias")
    fk_contratos = relationship("Contratos", back_populates="colonias")
    fk_colonia_rf = relationship("Reportes_Cli", back_populates="colonias")


    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ciudad': self.ciudad,
            'municipio': self.municipio,
            'asentamiento': self.asentamiento,
            'codigo_postal': self.codigo_postal,
        }
