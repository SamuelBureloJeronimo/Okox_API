from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Municipios(Base):
    __tablename__ = 'municipios'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    estado = Column(Integer, ForeignKey('estados.id'))
    
    # ForaignKey propias de la clase
    estados = relationship("Estados", back_populates="fk_municipios")
    # ForaignKey que apuntan a esta clase <-
    fk_colonias = relationship("Colonias", back_populates="municipios")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'estado': self.estado,
        }
