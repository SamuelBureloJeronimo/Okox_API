from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Colonias_Afectadas(Base):
    __tablename__ = 'colonias_afectadas'
    
    id_mantenimiento = Column(Integer, ForeignKey('mantenimientos.id'), primary_key=True, nullable=False)
    id_colonia = Column(Integer, ForeignKey('colonias.id'), primary_key=True, nullable=False)
    
    # ForaignKey propias de la clase
    colonias = relationship("Colonias", back_populates="fk_colonias_afectadas")
    mantenimientos = relationship("Mantenimientos", back_populates="fk_mantenimientos")
    
    def to_dict(self):
        return {
            'id_mantenimiento': self.id_mantenimiento,
            'id_colonia': self.id_colonia,
        }