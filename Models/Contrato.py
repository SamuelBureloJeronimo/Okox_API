from database.db import Base
from sqlalchemy import Column, Date, Integer, Float, String, func, ForeignKey
from sqlalchemy.orm import relationship

class Contratos(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rfc_cli = Column(String(13), ForeignKey('clientes.rfc'), nullable=False)
    fech_alta = Column(Date, default=func.now(), nullable=False)
    fech_vige = Column(Date, nullable=False)
    tipo_fact = Column(String(30), nullable=False)
    tipo_serv = Column(String(30), nullable=False)
    id_colonia = Column(Integer, ForeignKey('colonias.id'), nullable=False)  # Relación a una colonia (posiblemente otra tabla)

    Clientes = relationship("Clientes", backref="contratos")
    Colonias = relationship("Colonias", backref="contratos")

    def __init__(self, rfc_cli, fech_alta, fech_vige, tipo_fact, tipo_serv, id_colonia):
        self.rfc_cli = rfc_cli
        self.fech_alta = fech_alta
        self.fech_vige = fech_vige
        self.tipo_fact = tipo_fact
        self.tipo_serv = tipo_serv
        self.id_colonia = id_colonia

    def __repr__(self):
        return f"min={self.min}, max={self.max_L})"

    def __str__(self):
        return f"min={self.min}, max={self.max_L})"
    
    def to_dict(self):
        return {
            "rfc_cli": self.rfc_cli,
            "fech_alta": self.fech_alta,
            "fech_vige": self.fech_vige,
            "tipo_fact": self.tipo_fact,
            "tipo_serv": self.tipo_serv,
            "id_colonia": self.id_colonia
        }
