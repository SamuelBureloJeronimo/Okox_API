from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Mantenimientos(Base):
    __tablename__ = 'mantenimientos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rfc_tec = Column(String(13), ForeignKey('usuarios.rfc'))
    rfc_company = Column(String(13), ForeignKey('companies.rfc_user'))
    titulo = Column(String(80), nullable=False)
    descripcion = Column(String(200), nullable=False)
    fecha = Column(DateTime, nullable=False)
    
    # ForaignKey propias de la clase
    tecnico = relationship("Usuarios", foreign_keys="[Mantenimientos.rfc_tec]", back_populates="mantenimientos_tecnico")
    companies = relationship("Companies", back_populates="mantenimientos")
    # ForaignKey que apuntan a otra clase <-
    fk_mantenimientos = relationship("Colonias_Afectadas", back_populates="mantenimientos")
    
    def to_dict(self):
        return {
            'id': self.id,
            'rfc_tec': self.rfc_tec,
            'rfc_company': self.rfc_company,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha': self.fecha.isoformat(),
            'colonia_afectada': self.colonia_afectada,
        }
