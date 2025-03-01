from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database.db import Base

class Actions_Users(Base):
    __tablename__ = 'actions_users'
    
    fech = Column(DateTime, primary_key=True, default=func.now())
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    action = Column(String(100), nullable=True)
    
    def to_dict(self):
        return {
            'fech': self.fech,
            'session_id': self.session_id,
            'action': self.action
        }
