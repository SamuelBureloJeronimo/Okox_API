from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from database.db import *
from sqlalchemy import exc

from models.Companies import Companies
from models.Personas import Personas
from models.Usuarios import Usuarios

BP_Clientes = Blueprint('BP_Clientes', __name__, url_prefix='/clientes')

@BP_Clientes.route("/create", methods=["POST"])
def create_client():
    required_fields = ["rfc", "nombre", "app", "apm", "fech_nac", "sex", "id_colonia", "id_umbral", "id_company"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    persona = Personas(
        rfc=request.form.get("rfc"),
        nombre=request.form.get("nombre"),
        app=request.form.get("app"),
        apm=request.form.get("apm"),
        fech_nac=request.form.get("fech_nac"),
        sex=request.form.get("sex"),
        id_colonia=request.form.get("id_colonia")
    )

    user = Usuarios(
        rfc=request.form.get("rfc"),
        email=request.form.get("email"),
        username=request.form.get("username"),
        password=request.form.get("password"),
        id_company=request.form.get("id_company")
    )

    cliente = Clientes(
        rfc=request.form.get("rfc"),
        id_umbral=request.form.get("id_umbral"),
        id_company=request.form.get("id_company")
    )

    try:
        session.add(persona)
        session.add(cliente)
        session.add(user)
        session.add_all([persona, cliente, user])
        session.commit()
        return jsonify({"mensaje": "¡Nuevo cliente registrado con éxito!"}), 200
    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 

    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": "Error en la base de datos"
        }), 500