from datetime import datetime, timedelta
from flask import g
import jwt
from config.app import app
from database.db import *
from models.all_models import *

from functools import wraps
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from database.db import Session  # Importamos Session correctamente
from apscheduler.schedulers.background import BackgroundScheduler

def with_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session = Session()  # Crear nueva sesión por cada petición
        print("Sesión ABIERTA");
        try:
            response = f(session, *args, **kwargs)  # Pasamos la sesión
            session.commit()
            return response
        except IntegrityError as e:
            session.rollback()
            return jsonify({"error": "Error de integridad en la base de datos.", "detalle": str(e)}), 400
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": "Error en la base de datos.", "detalle": str(e)}), 500
        
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        
        finally:
            session.close()  # Cerramos la sesión siempre
            print("Sesión Cerrada");
    return decorated_function


def tarea_programada():
    with app.app_context():
        session = Session()
        
        # Fecha límite: hace 7 días
        hace_una_semana = datetime.now() - timedelta(days=7)
        inicio_dia = hace_una_semana.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_dia = hace_una_semana.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Usuarios que nunca han iniciado sesión
        usuarios_a_eliminar = session.query(Usuarios.rfc).filter(
            Usuarios.last_session == None
        ).all()

        # Extraer los RFCs de los usuarios a eliminar
        rfc_a_eliminar = [usuario.rfc for usuario in usuarios_a_eliminar]

        if usuarios_a_eliminar:
            # Primero eliminar los usuarios
            session.query(Usuarios).filter(Usuarios.rfc.in_(rfc_a_eliminar)).delete(synchronize_session=False)

            # Luego eliminar las personas
            nom = session.query(Personas).filter(Personas.rfc.in_(rfc_a_eliminar)).delete(synchronize_session=False)

            session.commit()
            print(f"[{datetime.now()}] {nom} - Usuarios eliminados con cuentas NO confirmadas.")
        else:
            print(f"[{datetime.now()}] Todos los usuarios han confirmado su cuenta.")
        
        session.close()


# Evitar que el scheduler se inicie dos veces
if not hasattr(app, 'scheduler_started'):
    scheduler = BackgroundScheduler()
    scheduler.add_job(tarea_programada, 'cron', hour=17, minute=47)
    scheduler.start()
    app.scheduler_started = True  # Marcar que el scheduler ya inició

if __name__ == '__main__':
    
    try:
        Base.metadata.create_all(engine)
        print("Tablas creadas correctamente")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
    
    try:
        # Intentar hacer una consulta simple para verificar la conexión
        connection = engine.connect()
        connection.close()
        print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print(f"Error de conexión: {e}")

    app.run(host='0.0.0.0', port=5000, debug=True)