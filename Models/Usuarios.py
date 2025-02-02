from database.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Usuarios(Base):
    __tablename__ = "usuarios"

    rfc = Column(String(13), ForeignKey('personas.rfc'), primary_key=True, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255))
    token = Column(String(255))
    rol = Column(Integer, default=0)  # 0 == Cliente, 1 == Capturista, 2 == Técnico, 3 == Administrador, 4 = Compañia
    last_session = Column(DateTime, nullable=True)

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Personas = relationship("Personas", backref="usuarios")

    def __init__(self, rfc, username, password, email, token=None, rol=0, last_session=None):
        self.rfc = rfc
        self.username = username
        self.password = password
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
            "token": self.token,
            "rol": self.rol,
            "last_session": self.last_session
        }
