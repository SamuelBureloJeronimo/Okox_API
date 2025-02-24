from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Boolean, DateTime, func

from sqlalchemy.orm import relationship
from database.db import Base


class Reportes_Fugas(Base):
    __tablename__ = 'reportes_fugas'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rfc_cli = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False)
    foto = Column(String(255), nullable=False)
    razon = Column(String(255), nullable=False)
    atendido = Column(Boolean, nullable=False, default=False)
    id_colonia = Column(Integer, ForeignKey('colonias.id'), nullable=False)
    fecha_subida = Column(DateTime, default=func.now(), nullable=False)
    
    # ForaignKey propias de la clase
    clientes = relationship("Usuarios", back_populates="fk_reportes_fugas")
    colonias = relationship("Colonias", back_populates="fk_colonia_rf")
    
    def to_dict(self):
        return {
            'id': self.id,
            'rfc_cli': self.rfc_cli,
            'foto': self.foto,
            'razon': self.razon,
            'atendido': self.atendido,
            'id_colonia': self.id_colonia
        }