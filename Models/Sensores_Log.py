from database.db import Base
from sqlalchemy import Column, Double, DateTime, String, ForeignKey, func
from sqlalchemy.orm import relationship

class Sensores_Log(Base):
    __tablename__ = "sensores_log"

    fecha = Column(DateTime, primary_key=True, nullable=False, default=func.now())  # Fecha y hora asociada a la presión
    Wifi_MacAddress = Column(String(17), ForeignKey('dispositivos.Wifi_MacAddress'), nullable=False)
    presion = Column(Double, nullable=False)
    caudal = Column(Double, nullable=False)
    litros_consumidos = Column(Double, nullable=False)

    Dispositivos = relationship("Dispositivos", backref="sensores_log")

    def __init__(self, Wifi_MacAddress, presion, caudal, litros_consumidos, fecha=None):
        self.Wifi_MacAddress = Wifi_MacAddress
        self.presion = presion
        self.caudal = caudal
        self.litros_consumidos = litros_consumidos
        self.fecha = fecha

    def __repr__(self):
        return f"Presion(id={self.id}, presion={self.presion}, cliente={self.id_cliente}, fecha={self.fecha})"

    def __str__(self):
        return f"Presión de {self.presion} registrada para el cliente {self.id_cliente}"
