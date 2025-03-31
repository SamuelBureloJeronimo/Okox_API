from functools import wraps
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import jwt

from database.db import Session

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
