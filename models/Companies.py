from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.db import Base


class Companies(Base):
    __tablename__ = 'companies'
    
    rfc_user = Column(String(13), primary_key=True, nullable=False)
    logo = Column(String(255), nullable=True, default="/companies/default_perfil.png")
    nombre = Column(String(50), nullable=True)
    telefono = Column(String(40), nullable=True)
    facebook = Column(String(150), nullable=True)
    linkedIn = Column(String(150), nullable=True)
    link_x = Column(String(150), nullable=True)
    descripcion = Column(Text, nullable=True)
    id_colonia = Column(Integer, ForeignKey('colonias.id'), nullable=True)
    
    # ForaignKey propias de la clase
    colonias = relationship("Colonias", back_populates="fk_companies")
    # ForaignKey que apuntan a esta clase <-
    mantenimientos = relationship("Mantenimientos", back_populates="companies")
    usuarios = relationship("Usuarios", back_populates="companies")
    
    def to_dict(self):
        return {
            'rfc_user': self.rfc_user,
            'logo': self.logo,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'facebook': self.facebook,
            'linkedIn': self.linkedIn,
            'link_x': self.link_x,
            'descripcion': self.descripcion,
            'id_colonia': self.id_colonia
        }
