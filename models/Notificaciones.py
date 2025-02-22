from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Notificaciones(Base):
    __tablename__ = 'notificaciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rfc_user = Column(String(13), ForeignKey('usuarios.rfc'))
    asunto = Column(String(80), nullable=False)
    descripcion = Column(String(200), nullable=False)
    tipo = Column(String(80), nullable=False)
    fecha_envio = Column(String(80), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuarios", back_populates="notificaciones")
    
    def to_dict(self):
        return {
            'id': self.id,
            'rfc_user': self.rfc_user,
            'asunto': self.asunto,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'fecha_envio': self.fecha_envio,
        }
