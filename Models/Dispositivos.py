from database.db import Base
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

class Dispositivos(Base):
    __tablename__ = "dispositivos"

    Wifi_MacAddress = Column(String(17), primary_key=True, unique=True)
    rfc = Column(String(13), ForeignKey('clientes.rfc'), nullable=False)
    valvula = Column(Boolean, default=False)
    last_connection = Column(DateTime, nullable=True)

    # Relación: cada estado está relacionado con un cliente
    Clientes = relationship("Clientes", backref="dispositivos")

    def __init__(self, Wifi_MacAddress, rfc, valvula=False, last_connection=None):
        self.Wifi_MacAddress = Wifi_MacAddress
        self.rfc = rfc
        self.valvula = valvula
        self.last_connection = last_connection

    def __repr__(self):
        return f"Dispositivo(Wifi_MacAddress={self.Wifi_MacAddress}, rfc={self.rfc})"

    def __str__(self):
        return f"Dispositivo {self.Wifi_MacAddress} asociado a cliente {self.rfc}"

    def to_dict(self):
        return {
            "Wifi_MacAddress": self.Wifi_MacAddress,
            "valvula": self.valvula,
            "rfc": self.rfc,
            "last_connection": self.last_connection
        }
