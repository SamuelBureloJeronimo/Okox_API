from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required
from config.middlewares import with_session
from database.db import *
from models.Bandeja import Bandejas
from models.Dispositivos import Dispositivos
from models.Personas import Personas
from models.Sensores_Log import Sensores_Log
from sqlalchemy import exc, func
from sqlalchemy.orm import aliased

from models.Usuarios import Usuarios
from models.address.Colonias import Colonias
from models.address.Estados import Estados
from models.address.Municipios import Municipios

BP_Technician = Blueprint('BP_Technician', __name__, url_prefix="/technician")

@BP_Technician.route('/inbox-all', methods=['GET'])
@jwt_required()
@with_session
def connect_device(session):
    
    bandejas = session.query(Bandejas).all();

    # Convertir lista de objetos en lista de diccionarios
    bandejas_list = [band.to_dict() for band in bandejas]

    return jsonify(bandejas_list), 200

@BP_Technician.route("/register-device", methods=["POST"])
@jwt_required()
@with_session
def create_device(session):
    required_fields = ["rfc", "dir_mac"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    device = Dispositivos(
        Wifi_MacAddress=request.form.get("dir_mac"),
        rfc_cli=request.form.get("rfc")
    )
    session.query(Bandejas).filter(Bandejas.Wifi_MacAddress == device.Wifi_MacAddress).delete()
    session.add(device)
    session.commit()
    return jsonify({"mensaje": "¡Nuevo dispositivo registrado con éxito!"}), 200

@BP_Technician.route('/get-clients/<rfc>', methods=['GET'])
@jwt_required()
@with_session
def get_clients(session, rfc):

    # Alias para evitar conflictos en la consulta
    persona_alias = aliased(Personas)


    client = session.query(Usuarios.email, Usuarios.last_session, persona_alias).join(persona_alias, Usuarios.rfc == persona_alias.rfc)\
    .filter((Usuarios.rol == 0) & (persona_alias.rfc == rfc)).first();

    if client is None:
        return jsonify("No hay ningun cliente con ese RFC."), 400

    email, last_session, persona = client  # Desempaquetar la tupla
    # Unir los datos de Usuarios y Personas en un solo objeto JSON
    resultado = {
        "email": email, "last_session": last_session,
        **(persona.to_dict() if persona else {})  # Agregar datos de Personas
    }
    dom_query = session.query(Colonias, Municipios, Estados)\
            .join(Municipios, Municipios.id == Colonias.municipio)\
            .join(Estados, Estados.id == Municipios.estado)\
            .filter(Colonias.id == persona.id_colonia)\
            .first()
    colonia, municipio, estado = dom_query
    dom = {
                "colonia": colonia.to_dict(),
                "municipio": municipio.to_dict(),
                "estado": estado.to_dict()
            }

    return jsonify({"user": resultado, "dom": dom}), 200

