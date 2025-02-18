from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from database.db import Base
from datetime import datetime

class Pagos(Base):
    __tablename__ = 'pagos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rfc_cli = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False)
    comprobante = Column(String(255), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_pago = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_subida = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relaciones
    cliente = relationship("Usuarios", back_populates="pagos")
    
    def to_dict(self):
        """Método para serializar el modelo a diccionario."""
        return {
            'id': self.id,
            'rfc_cli': self.rfc_cli,
            'comprobante': self.comprobante,
            'monto': self.monto,
            'fecha_pago': self.fecha_pago.isoformat(),
            'fecha_subida': self.fecha_subida.isoformat(),
        }