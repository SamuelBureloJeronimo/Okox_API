from database.db import Base
from sqlalchemy import Column, String, Text, ForeignKey, LargeBinary, Integer
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rfc = Column(String(13), ForeignKey('personas.rfc'), unique=True, nullable=False)  
    logo = Column(String(255))
    nombre = Column(String(50))
    descripcion = Column(Text)
    facebook = Column(String(150))
    linkedIn = Column(String(150))
    link_x = Column(String(150))

    Personas = relationship("Personas", backref="owners")

    def __init__(self, rfc, logo, nombre, descripcion, facebook, linkedIn, link_x):
        self.rfc = rfc
        self.logo = logo
        self.nombre = nombre
        self.descripcion = descripcion
        self.facebook = facebook
        self.linkedIn = linkedIn
        self.link_x = link_x

    def __repr__(self):
        return f"rfc={self.rfc}, nombre={self.nombre})"

    def __str__(self):
        return f"nombre={self.nombre}, nombre={self.nombre})"
    
    def to_dict(self):
        return {
            "rfc": self.rfc,
            "logo": self.logo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "facebook": self.facebook,
            "linkedIn": self.linkedIn,
            "link_x":  self.link_x
        }