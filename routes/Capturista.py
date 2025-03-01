from datetime import datetime, timedelta
import secrets
import string
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from database.db import *
from sqlalchemy.orm import aliased
from index import with_session
from models.Contratos import Contratos
from models.Personas import Personas
from models.Usuarios import Usuarios


BP_Capturista = Blueprint('BP_Capturista', __name__, url_prefix='/capturista')

@BP_Capturista.route('/create-cliente', methods=['POST'])
@with_session
@jwt_required()
def create_client(session):
    required_fields = ["rfc", "nombre", "app", "apm", "fech_nac", "sex", "id_colonia", "tel"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    id_company = jwt_data.get("id_company")  # Si guardaste "nombre" en el token

    
    persona = Personas()
    persona.rfc=request.form.get("rfc"),
    persona.nombre=request.form.get("nombre"),
    persona.app=request.form.get("app"),
    persona.apm=request.form.get("apm"),
    persona.fech_nac=request.form.get("fech_nac"),
    persona.tel=request.form.get("tel"),
    persona.sex=request.form.get("sex"),
    persona.id_colonia=request.form.get("id_colonia")


    user = Usuarios()
    user.rfc=request.form.get("rfc"),
    user.email=request.form.get("email"),
    user.username="username_"+str(persona.rfc),
    user.password=gn_pass(7),
    user.id_company=id_company

    exist_rfc = session.query(Usuarios).filter_by(rfc=user.rfc).first();

    exist_email = session.query(Usuarios).filter_by(email=user.email).first();

    if exist_email:
        return jsonify({"error": "¡Este email ya ha sido registrado!"}), 201
    if exist_rfc:
        return jsonify({"error": "¡El RFC ya esta asociado a un cliente!"}), 201

    session.add_all([persona, user])
    session.commit()
    return jsonify({"mensaje": "¡Nuevo cliente registrado con éxito!"}), 200

@BP_Capturista.route('/create-contract', methods=["POST"])
@jwt_required()
@with_session
def create_contract(session):
    
    required_fields = ["rfc_cli", "tipo_fact", "max_L", "colonia"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

    contrato = Contratos()
    contrato.rfc_cli = request.form.get("rfc_cli");
    contrato.fech_alta = datetime.now();
    contrato.fech_vige = datetime.now() + timedelta(days=365);
    contrato.tipo_serv = "Domestico";
    contrato.tipo_fact = request.form.get("tipo_fact");
    contrato.max_L = request.form.get("max_L");
    contrato.id_colonia = request.form.get("colonia");

    session.add(contrato)
    session.commit()
    return jsonify("Nuevo contrato generado"), 200

@BP_Capturista.route('/get-all-clients', methods=["GET"])
def get_all_clients():

    # Alias para evitar conflictos en la consulta
    persona_alias = aliased(Personas)

    # Hacemos el JOIN con Personas
    users = session.query(Usuarios, persona_alias).join(persona_alias, Usuarios.rfc == persona_alias.rfc)\
    .filter(Usuarios.rol == 0).all()

    # Convertir a lista de diccionarios sin escribir campo por campo
    users_list = [
        {**usuario.__dict__, **persona.__dict__}
        for usuario, persona in users
    ]

    # Eliminar claves internas de SQLAlchemy (que inician con '_')
    for user in users_list:
        user.pop('_sa_instance_state', None)

    return jsonify(users_list), 200


def gn_pass(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))