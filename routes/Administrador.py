import secrets
import string
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from config.middlewares import with_session
from database.db import *
from models.Mantenimientos import Mantenimientos
from models.Personas import Personas
from models.Usuarios import Usuarios
from sqlalchemy.orm import aliased


BP_Administracion = Blueprint('BP_Administracion', __name__, url_prefix='/admin')

@BP_Administracion.route('/create-user', methods=['POST'])
@jwt_required()
@with_session
def create_new_user(session):
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
    session.add_all([persona, user])
    session.commit()
    return jsonify({"mensaje": "¡Nuevo usuario a sido registrado con éxito!"}), 200

    
@BP_Administracion.route('/get-users', methods=['GET'])
@jwt_required()
@with_session
def get_users(session):
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    
    rol = jwt_data.get("sub") 

    if rol != "3":
        return jsonify("No tienes permisos de acceso"), 401
    # Alias para evitar conflictos en la consulta
    persona_alias = aliased(Personas)

    # Hacemos el JOIN con Personas
    users = session.query(Usuarios, persona_alias)\
        .join(persona_alias, Usuarios.rfc == persona_alias.rfc)\
    .filter((Usuarios.rol > 0) & (Usuarios.rol < 3)).all()

    # Convertir a lista de diccionarios sin escribir campo por campo
    users_list = [
        {**usuario.__dict__, **persona.__dict__}
        for usuario, persona in users
    ]

    # Eliminar claves internas de SQLAlchemy (que inician con '_')
    for user in users_list:
        user.pop('_sa_instance_state', None)

    return jsonify(users_list), 200

@BP_Administracion.route('/search-tec/<rfc>', methods=['GET'])
@jwt_required()
@with_session
def search_tec(session, rfc):
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    rol = jwt_data.get("sub") 

    if rol != "3":
        return jsonify("No tienes permisos de acceso"), 401

    # Hacemos un JOIN con la tabla personas para obtener el nombre del usuario
    techn = session.query(Usuarios, Personas.nombre, Personas.app, Personas.apm).join(Personas, Personas.rfc == Usuarios.rfc)\
        .filter_by(rfc=rfc).first()

    if techn is None:
        return jsonify("No se encontro usuario con ese rfc"), 400
    
    # Convertir lista de tuplas en lista de diccionarios
    usuario_obj, nombre, app, apm = techn
    user_data = {
        **usuario_obj.to_dict(),  # Desempaquetamos el diccionario original
        "nombre": nombre +" "+ app +" "+ apm
    } 

    if usuario_obj.rol != 2:
        return jsonify("Este usuario no es un técnico"), 400

    return jsonify(user_data), 200


@BP_Administracion.route('/register-manten', methods=['POST'])
@jwt_required()
@with_session
def register_manten(session):
    required_fields = ["rfc_tec", "titulo", "descripcion", "fecha", "col_afec"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT

    id_company = jwt_data.get("id_company")  # Si guardaste "nombre" en el token
    rol = jwt_data.get("sub") 

    if rol != "3":
        return jsonify("No tienes permisos de acceso"), 401

    mantenimiento = Mantenimientos(
        rfc_company=id_company,
        rfc_tec=request.form.get("rfc_tec"),
        titulo=request.form.get("titulo"),
        descripcion=request.form.get("descripcion"),
        fecha=request.form.get("fecha"),
        col_afec=request.form.get("col_afec")
    )

    session.add(mantenimiento)
    session.commit()
    return jsonify("¡El mantenimiento se registro correctamente"), 200



    
def gn_pass(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))