from database.db import Base
from sqlalchemy import Column, Integer, Float

class Umbral_Clientes(Base):
    __tablename__ = "umbral_clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    min_L = Column(Float, default=0, nullable=False)
    max_L = Column(Float, default=0, nullable=False)
    

    def __init__(self, min_L, max_L):
        self.min_L = min_L
        self.max_L = max_L

    def __repr__(self):
        return f"min={self.min}, max={self.max_L})"

    def __str__(self):
        return f"min={self.min}, max={self.max_L})"
