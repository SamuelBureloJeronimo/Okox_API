from database.db import Base
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

class Sensores_Log(Base):
    __tablename__ = "sensores_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Wifi_MacAddress = Column(String(17), ForeignKey('dispositivos.Wifi_MacAddress'), nullable=False)
    presion = Column(Float, nullable=False, default=0.0)
    fecha = Column(DateTime, nullable=False)  # Fecha y hora asociada a la presión

    Dispositivos = relationship("Dispositivos", backref="sensores_log")

    def __init__(self, presion=0.0, id_cliente=0, fecha=None):
        self.presion = presion
        self.id_cliente = id_cliente
        self.fecha = fecha

    def __repr__(self):
        return f"Presion(id={self.id}, presion={self.presion}, cliente={self.id_cliente}, fecha={self.fecha})"

    def __str__(self):
        return f"Presión de {self.presion} registrada para el cliente {self.id_cliente}"
