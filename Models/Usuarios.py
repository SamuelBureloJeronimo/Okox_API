from database.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_persona = Column(String(13), ForeignKey('personas.rfc'), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=False)
    password = Column(String(255), nullable=False)
    token = Column(String(255), nullable=True)
    rol = Column(Integer, default=0)  # 0 == Cliente, 1 == Capturista, 2 == Técnico, 3 == Administrador
    last_session = Column(DateTime, nullable=True)

    # Relación: cada estado está relacionado con un Pais (con un Pais específico)
    Personas = relationship("Personas", backref="usuarios")

    def __init__(self, id_persona, username, password, token=None, rol=0, last_session=None):
        self.id_persona = id_persona
        self.username = username
        self.password = password
        self.token = token
        self.rol = rol
        self.last_session = last_session

    def __repr__(self):
        return f"Usuario({self.username}, rol={self.rol})"

    def __str__(self):
        return self.username
