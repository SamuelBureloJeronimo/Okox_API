from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Text
from database.db import Base

class Posts(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tittle = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    path_file = Column(String(255), nullable=False)
    url_face = Column(String(255), nullable=False)
    type = Column(Boolean, nullable=False)
    fech_alta = Column(DateTime, default=func.now(), nullable=False)
    
    
    def to_dict(self):
        """Método para serializar el modelo a diccionario."""
        return {
            'id': self.id,
            'tittle': self.tittle,
            'description': self.description,
            'path_file': self.path_file,
            'url_face': self.url_face,
            'type': self.type,
            'fech_alta': self.fech_alta
        }