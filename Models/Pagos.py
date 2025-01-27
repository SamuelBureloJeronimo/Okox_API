from database.db import Base
from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import relationship

class Pagos(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rfc = Column(String(13), ForeignKey("clientes.rfc"), nullable=False)
    comprobante = Column(LargeBinary(length=16777215), nullable=False)
    monto = Column(Float, nullable=False, default=0.0)  # Monto del pago
    fecha_pago = Column(DateTime, nullable=False)  # Fecha del pago
    fecha_subida = Column(DateTime, nullable=False)  # Fecha de subida

    Clientes = relationship("Clientes", backref="pagos")

    def __init__(self, rfc, comprobante, monto, fecha_pago, fecha_subida):
        self.rfc = rfc
        self.comprobante = comprobante
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.fecha_subida = fecha_subida


    def __repr__(self):
        return f"Pago(id={self.id}, rfc={self.rfc}, fecha={self.fecha_pago}, monto={self.monto})"

    def __str__(self):
        return f"Pago de {self.monto} realizado por el cliente {self.rfc} el {self.fecha_pago}"
