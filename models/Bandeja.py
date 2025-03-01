from sqlalchemy import Column, String, DateTime, func, Double, Boolean
from database.db import Base

class Bandejas(Base):
    __tablename__ = 'bandejas'
    
    Wifi_MacAddress = Column(String(17), primary_key=True, nullable=False)
    fecha = Column(DateTime, default=func.now(), nullable=False)
    ip_client = Column(String(30), nullable=False)
    
    def to_dict(self):
        return {
            'Wifi_MacAddress': self.Wifi_MacAddress,
            'fecha': self.fecha.isoformat() if self.fecha else None,  # Usamos isoformat() para convertir el datetime a string
            'ip_client': self.ip_client
        }
