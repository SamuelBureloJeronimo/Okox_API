import secrets
import string
from flask import Blueprint, jsonify, request
from flask_jwt_extended import decode_token, get_jwt, get_jwt_identity, jwt_required
from database.db import *
from sqlalchemy import exc
from models.Companies import Companies
from models.Personas import Personas
from models.Usuarios import Usuarios


BP_Administracion = Blueprint('BP_Administracion', __name__, url_prefix='/admin')

@BP_Administracion.route('/create-user', methods=['POST'])
@jwt_required()
def create_new_user():
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    
    id_company = jwt_data.get("id_company")  # Si guardaste "nombre" en el token


    # Obtener el token desde el encabezado o cuerpo de la solicitud
    token = request.headers.get('Authorization')

    # Remover el prefijo "Bearer " si está presente
    if token.startswith("Bearer "):
        token = token.split("Bearer ")[1]

    required_fields = ["rfc", "nombre", "app", "apm", "fech_nac", "sex", "id_colonia", "rol", "tel", "email"]
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
        id_company=id_company
    )
    try:
        session.add(persona)
        session.add(user)
        session.add_all([persona, user])
        session.commit()
        return jsonify({"mensaje": "¡Nuevo usuario a sido registrado con éxito!", "user": user.username, "pass": user.password}), 200
    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 500 
    

def gn_pass(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))