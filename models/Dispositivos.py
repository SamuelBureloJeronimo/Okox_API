from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Dispositivos(Base):
    __tablename__ = 'dispositivos'
    
    Wifi_MacAddress = Column(String(17), primary_key=True, nullable=False)
    rfc_cli = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False)
    valvula = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True)
    last_connection = Column(DateTime)
    
    # Relaciones
    cliente = relationship("Usuarios", back_populates="dispositivos")
    sensores_log = relationship("Sensores_Log", back_populates="dispositivo")
    
    def to_dict(self):
        return {
            'Wifi_MacAddress': self.Wifi_MacAddress,
            'rfc_cli': self.rfc_cli,
            'valvula': self.valvula,
            'last_connection': self.last_connection.isoformat() if self.last_connection else None,
        }
