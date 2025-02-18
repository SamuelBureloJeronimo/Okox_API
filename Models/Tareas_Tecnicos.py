from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Tareas_Tecnicos(Base):
    __tablename__ = 'tareas_tecnicos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rfc_tec = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False, default='')
    nombre = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_asignacion = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime)
    estado = Column(String(20), nullable=False)
    prioridad = Column(String(20), nullable=False)
    evidencia = Column(String(255))
    observaciones = Column(Text)
    
    # Relaciones
    tecnico = relationship("Usuarios", back_populates="fk_tareas_tecnicos")
    
    def to_dict(self):
        return {
            'id': self.id,
            'rfc_tec': self.rfc_tec,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_asignacion': self.fecha_asignacion.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'evidencia': self.evidencia,
            'observaciones': self.observaciones,
        }
