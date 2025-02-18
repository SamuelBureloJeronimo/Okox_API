from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Estados(Base):
    __tablename__ = 'estados'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    pais = Column(Integer, ForeignKey('paises.id'))
    
    # ForaignKey propias de la clase
    paises = relationship("Paises", back_populates="fk_estados")
    # ForaignKey que apuntan a esta clase <-
    fk_municipios = relationship("Municipios", back_populates="estados")

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'pais': self.pais,
        }
