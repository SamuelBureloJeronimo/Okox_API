from sqlalchemy import Column, String, DateTime, Integer, Time, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from database.db import Base

class Visitas(Base):
    __tablename__ = 'visitas'
    
    fecha = Column(DateTime, primary_key=True, default=func.now())
    url = Column(String(255), nullable=False)
    ip_user = Column(String(50), nullable=False)
    tiempo_carga = Column(Float, nullable=False)
    duracion = Column(Float, nullable=False)
    rfc_user = Column(String(13), nullable=True)
    origin = Column(String(100), nullable=False)
    id_session = Column(String(100), nullable=False)
    
    def to_dict(self):
        return {
            'fecha': self.id,
            'url': self.url,
            'ip_user': self.ip_user,
            'tiempo_carga': self.tiempo_carga,
            'duracion': self.duracion,
            'rfc_user': self.rfc_user,
            'origin': self.origin,
            'id_session': self.id_session,
        }