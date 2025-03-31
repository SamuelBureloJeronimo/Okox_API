from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Colonias(Base):
    __tablename__ = 'colonias'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nom = Column(String(100), nullable=False)
    ciud = Column(String(100), nullable=False)
    mun_id = Column(Integer, ForeignKey('municipios.id'))
    asen = Column(String(100))
    cp = Column(Integer)
    
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
            'nom': self.nom,
            'ciud': self.ciud,
            'mun_id': self.mun_id,
            'asen': self.asen,
            'cp': self.cp,
        }
