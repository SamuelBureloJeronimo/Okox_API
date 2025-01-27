from database.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Suspensiones(Base):
    __tablename__ = "suspensiones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rfc = Column(String(13), ForeignKey("clientes.rfc"), nullable=False)
    motivo_id = Column(Integer, ForeignKey("motivo_suspensiones.id"), nullable=False)
    duracion_suspension = Column(DateTime, nullable=False)  # Representa una duración o tiempo específico
    fecha = Column(DateTime, nullable=False)  # Fecha y hora de la suspensión

    Clientes = relationship("Clientes", backref="suspensiones");
    Motivo_Suspensiones = relationship("Motivo_Suspensiones", backref="suspensiones");

    def __init__(self, motivo_id, duracion_suspension, id_cliente, fecha):
        self.motivo_id = motivo_id
        self.duracion_suspension = duracion_suspension
        self.id_cliente = id_cliente
        self.fecha = fecha

    def __repr__(self):
        return f"Suspension(motivo={self.motivo_id}, cliente={self.id_cliente}, fecha={self.fecha})"

    def __str__(self):
        return f"Suspension por: {self.motivo_id}"
