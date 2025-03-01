from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from database.db import Base

class Actividades(Base):
    __tablename__ = 'actividades'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rfc_admin = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False, unique=True, comment='RFC de la persona que asignó la tarea')
    rfc_techn = Column(String(13), ForeignKey('usuarios.rfc'), nullable=False, unique=True, comment='RFC del empleado al que se le asignó la tarea')
    titulo = Column(String(100), nullable=False, comment='Nombre de la actividad. Ejemplo: Limpieza de zona, rellenar biberes')
    desc = Column(String(255), comment='Descripción de la tarea por si se necesitan más indicaciones')
    fech_in = Column(DateTime, nullable=False, comment='Fecha de inicio de la tarea en día y hora')
    fech_fi = Column(DateTime, nullable=False, comment='Fecha máxima de finalización')
    estado = Column(Integer, nullable=False, default=0, comment='0 = Pendiente, 1 = Atendiendo, 2 = Completada, 3 = Verificada, 4 = Inconcluso')
    observ = Column(Text, comment='Si hubo algún problema aquí se describe')

    def to_dict(self):
        return {
            "rfc_admin": self.rfc_admin,
            "rfc_techn": self.rfc_techn,
            "titulo": self.titulo,
            "desc": self.desc,
            "fech_in": self.fech_in.isoformat() if self.fech_in else None,
            "fech_fi": self.fech_fi.isoformat() if self.fech_fi else None,
            "estado": self.estado,
            "observ": self.observ
        }