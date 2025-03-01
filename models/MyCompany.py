from sqlalchemy import Column, String
from database.db import Base


class MyCompany(Base):
    __tablename__ = 'my_company'
    
    rfc = Column(String(13), primary_key=True, nullable=False)
    logo = Column(String(255), nullable=True, default="/company/default_perfil.png")
    nombre = Column(String(50), nullable=True)
    
    
    def to_dict(self):
        return {
            'rfc': self.rfc,
            'logo': self.logo,
            'nombre': self.nombre
        }
