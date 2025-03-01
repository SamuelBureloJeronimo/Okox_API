from sqlalchemy import Column, String, Double, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database.db import Base

class Sensores_Log(Base):
    __tablename__ = 'sensores_log'
    
    fecha = Column(DateTime, primary_key=True, default=func.now(), nullable=False)
    Wifi_MacAddress = Column(String(17), ForeignKey('dispositivos.Wifi_MacAddress'), nullable=False)
    presion = Column(Double, nullable=False, default=0)
    caudal = Column(Double, nullable=False, default=0)
    litros_consumidos = Column(Double, nullable=False, default=0)
    
    # Relaciones
    dispositivo = relationship("Dispositivos", back_populates="sensores_log")
    
    def to_dict(self):
        return {
            'fecha': self.fecha.isoformat(),
            'Wifi_MacAddress': self.Wifi_MacAddress,
            'presion': self.presion,
            'caudal': self.caudal,
            'litros_consumidos': self.litros_consumidos,
        }
