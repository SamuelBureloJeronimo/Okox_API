from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship, backref

class Personas(Base):
    __tablename__ = 'personas'
    
    rfc = Column(String(13), primary_key=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    app = Column(String(100), nullable=False)
    apm = Column(String(100), nullable=False)
    fech_nac = Column(Date, nullable=False)
    sex = Column(String(1), nullable=False)
    tel = Column(String(25), nullable=False, default='')
    id_colonia = Column(Integer, ForeignKey('colonias.id'), nullable=False)
    
    # Relaciones
    colonias = relationship("Colonias", back_populates="fk_personas")
    
    def to_dict(self):
        return {
            'rfc': self.rfc,
            'nombre': self.nombre,
            'app': self.app,
            'apm': self.apm,
            'fech_nac': self.fech_nac.strftime('%Y-%m-%d') if self.fech_nac else None,
            'sex': self.sex,
            'id_colonia': self.id_colonia,
            'tel': self.tel
        }