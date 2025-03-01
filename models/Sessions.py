from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from database.db import Base
from sqlalchemy.sql import expression

class Sessions(Base):
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    rfc_user = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False)
    fech_conn = Column(DateTime, default=func.now())
    fech_disc = Column(DateTime, default=expression.text("(NOW() + INTERVAL 30 MINUTE)"))
    
    def to_dict(self):
        return {
            'id': self.id,
            'rfc_user': self.rfc_user,
            'fech_conn': self.fech_conn,
            'fech_disc': self.fech_disc
        }
