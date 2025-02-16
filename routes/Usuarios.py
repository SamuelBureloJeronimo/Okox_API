import secrets
import string
from flask import Blueprint, jsonify, request
from database.db import *
from sqlalchemy import exc
from models.Personas import Personas
from models.Usuarios import Usuarios


BP_Usuarios = Blueprint('BP_Usuarios', __name__)

@BP_Usuarios.route('/admin/create-user', methods=['POST'])
def create_new_user():
    required_fields = ["rfc", "nombre", "app", "apm", "fech_nac", "sex", "id_colonia", "rol", "tel", "email", "id_company"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    us_exist = session.query(Usuarios).get(request.form.get("rfc"))

    if us_exist:
        return jsonify({"msg": "Este RFC ya esta registrado"}), 400


    persona = Personas(
        rfc=request.form.get("rfc"),
        nombre=request.form.get("nombre"),
        app=request.form.get("app"),
        apm=request.form.get("apm"),
        tel=request.form.get("tel"),
        fech_nac=request.form.get("fech_nac"),
        sex=request.form.get("sex"),
        id_colonia=request.form.get("id_colonia")
    )

    user = Usuarios(
        rfc=request.form.get("rfc"),
        email=request.form.get("email"),
        username="user_"+persona.rfc,
        password=gn_pass(7),
        rol=request.form.get("rol"),
        id_company=request.form.get("id_company")
    )

    try:
        session.add(persona)
        session.add(user)
        session.add_all([persona, user])
        session.commit()
        return jsonify({"mensaje": "¡Nuevo usuario a sido registrado con éxito!" , "pass": user.password}), 200
    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 

    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 500
    

def gn_pass(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))