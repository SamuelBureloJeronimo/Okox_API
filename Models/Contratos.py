from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Contratos(Base):
    __tablename__ = 'contratos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rfc_cli = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False)
    fech_alta = Column(Date, nullable=False)
    fech_vige = Column(Date, nullable=False)
    tipo_fact = Column(String(30), nullable=False)
    tipo_serv = Column(String(30), nullable=False)
    min_L = Column(Float, nullable=False)
    max_L = Column(Float, nullable=False)
    id_colonia = Column(Integer, ForeignKey('colonias.id'), nullable=False)
    
    # Relaciones
    cliente = relationship("Usuarios", back_populates="contratos")
    colonias = relationship("Colonias", back_populates="fk_contratos")
    
    def to_dict(self):
        return {
            'id': self.id,
            'rfc_cli': self.rfc_cli,
            'fech_alta': self.fech_alta.isoformat(),
            'fech_vige': self.fech_vige.isoformat(),
            'tipo_fact': self.tipo_fact,
            'tipo_serv': self.tipo_serv,
            'min_L': self.min_L,
            'max_L': self.max_L,
            'id_colonia': self.id_colonia,
        }
