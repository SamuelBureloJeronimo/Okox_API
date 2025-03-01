from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database.db import Base

class Usuarios(Base):
    __tablename__ = 'usuarios'

    # Columnas de la tabla
    rfc = Column(String(50), ForeignKey('personas.rfc'), primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255))
    rol = Column(Integer, default='0',comment='# 0 == Cliente, 1 == Capturista, 2 == Técnico, 3 == Administrador, 4 = Compañia')
    last_session = Column(DateTime)
    fech_created = Column(DateTime, default=func.now(), nullable=False)
    imagen = Column(String(255), default='/clients/default_perfil.png')
    id_company = Column(String(13), ForeignKey('companies.rfc_user'))

    # ForaignKey propias de la clase
    companies = relationship("Companies", back_populates="usuarios")
    contratos = relationship("Contratos", back_populates="cliente")
    dispositivos = relationship("Dispositivos", back_populates="cliente")
    mantenimientos_tecnico = relationship("Mantenimientos", foreign_keys="[Mantenimientos.rfc_tec]", back_populates="tecnico")
    notificaciones = relationship("Notificaciones", back_populates="usuario")
    pagos = relationship("Pagos", back_populates="cliente")
    fk_reportes_fugas = relationship("Reportes_Cli", back_populates="clientes")
    fk_suspensiones = relationship("Suspensiones", back_populates="usuarios")
    fk_tareas_tecnicos = relationship("Tareas_Tecnicos", back_populates="tecnico")

    # Método para convertir el objeto en un diccionario serializable
    def to_dict(self):
        return {
            'rfc': self.rfc,
            'email': self.email,
            'username': self.username,
            'password': self.password,  # ¡Cuidado! No deberías exponer contraseñas en APIs.
            'rol': self.rol,
            'last_session': self.last_session.isoformat() if self.last_session else None,
            'fech_created': self.fech_created.isoformat() if self.fech_created else None,
            'imagen': self.imagen,
            'id_company': self.id_company
        }

    # Método opcional para representación en cadena (útil para debugging)
    def __repr__(self):
        return f"<Usuario(rfc={self.rfc}, email={self.email}, username={self.username}, rol={self.rol})>"