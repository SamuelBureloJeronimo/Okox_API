from database.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

class Usuarios(Base):
    __tablename__ = "usuarios"

    rfc = Column(String(13), ForeignKey('personas.rfc'), primary_key=True, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255))
    token = Column(Text)
    imagen = Column(String(255), default="blank-profile-picture-973460_960_720.png")
    rol = Column(Integer, default=0)  # 0 == Cliente, 1 == Capturista, 2 == Técnico, 3 == Administrador, 4 = Compañia
    last_session = Column(DateTime, nullable=True)
    id_company = Column(Integer, ForeignKey('company.id'), nullable=False)

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Personas = relationship("Personas", backref="usuarios")
    Company = relationship("Company", backref="company")

    def __init__(self, rfc, username, password, email, id_company, token=None, rol=0, last_session=None):
        self.rfc = rfc
        self.username = username
        self.password = password
        self.id_company = id_company
        self.email = email
        self.token = token
        self.rol = rol
        self.last_session = last_session

    def __repr__(self):
        return f"Usuario({self.username}, rol={self.rol})"

    def __str__(self):
        return self.username
    
    def to_dict(self):
        return {
            "rfc": self.rfc,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "id_company": self.id_company,
            "token": self.token,
            "imagen": self.imagen,
            "rol": self.rol,
            "last_session": self.last_session
        }
