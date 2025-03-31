from sqlalchemy import Column, Integer, String
from database.db import Base
from sqlalchemy.orm import relationship

class Paises(Base):
    __tablename__ = 'paises'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nom = Column(String(100), nullable=False)

    # ForaignKey que apuntan a esta clase <-
    fk_estados = relationship("Estados", back_populates="paises")

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
        }
