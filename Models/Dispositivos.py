from database.db import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Dispositivos(Base):
    __tablename__ = "dispositivos"

    Wifi_MacAddress = Column(String(17), primary_key=True, unique=True)
    rfc = Column(String(13), ForeignKey('clientes.rfc'), nullable=False)  # Relación al cliente que tiene el dispositivo
    
    # Relación: cada estado está relacionado con un cliente
    Clientes = relationship("Clientes", backref="dispositivos")

    def __init__(self, rfc):
        self.rfc = rfc

    def __repr__(self):
        return f"Dispositivo(Wifi_MacAddress={self.Wifi_MacAddress}, rfc={self.rfc})"

    def __str__(self):
        return f"Dispositivo {self.Wifi_MacAddress} asociado a cliente {self.rfc}"

    def to_dict(self):
        return {
            "Wifi_MacAddress": self.Wifi_MacAddress,
            "rfc": self.rfc,
        }
