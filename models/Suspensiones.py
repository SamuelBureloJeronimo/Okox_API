from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class Suspensiones(Base):
    __tablename__ = 'suspensiones'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rfc = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False)
    motivo = Column(String(50), nullable=False)
    duracion_suspension = Column(DateTime, nullable=False)
    fecha = Column(DateTime, nullable=False, default=func.now())
    
    # Relaciones
    usuarios = relationship("Usuarios", back_populates="fk_suspensiones")
    
    def to_dict(self):
        """Método para serializar el modelo a diccionario."""
        return {
            'id': self.id,
            'rfc': self.rfc,
            'motivo': self.motivo,
            'duracion_suspension': self.duracion_suspension.isoformat(),
            'fecha': self.fecha.isoformat(),
        }