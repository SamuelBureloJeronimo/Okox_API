from random import randint
import uuid
from flask import Blueprint, request, jsonify
from database.db import *
from sqlalchemy import exc
from werkzeug.utils import secure_filename

import os

from models.Company import Company
from models.Personas import Personas
from models.Usuarios import Usuarios

# Cargar variables desde el archivo .env
load_dotenv()

BP_Company = Blueprint('BP_Company', __name__, url_prefix='/company')

@BP_Company.route('/create', methods=['POST'])
def create_owner():
    required_fields = ["rfc", "nombre", "app", "apm", "fech_nac", "sex", "id_colonia", "nombre_empresa", "descripcion"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

    # Validar si la imagen está presente
    if 'logo' not in request.files:
        return jsonify({"error": "El campo 'logo' es obligatorio"}), 400

    persona = Personas(
        rfc=request.form.get("rfc"),
        nombre=request.form.get("nombre"),
        app=request.form.get("app"),
        apm=request.form.get("apm"),
        fech_nac=request.form.get("fech_nac"),
        sex=request.form.get("sex"),
        id_colonia=request.form.get("id_colonia")
    )
    # Procesar la imagen
    if 'logo' in request.files:
        file = request.files['logo']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_nombre = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER")+"image/", nuevo_nombre)
        
        file.save(filepath)  # Guardar el archivo
    else:
        filepath = None

    company = Company(
        rfc=request.form.get("rfc"),
        logo=nuevo_nombre,
        nombre=request.form.get("nombre_empresa"),
        descripcion=request.form.get("descripcion"),
        facebook=request.form.get("facebook"),
        linkedIn=request.form.get("linkedIn"),
        link_x=request.form.get("link_x")
    )

    user = Usuarios(
        rfc=request.form.get("rfc"),
        username=request.form.get("username"),
        password=request.form.get("password"),
        email=request.form.get("email"),
        rol=4
    )
    
    try:
        session.add(persona)
        session.add(company)
        session.add(user)
        session.add_all([persona, company, user])
        session.commit()
        return jsonify({"mensaje": "¡Nueva compañia registrada con éxito!"}), 200
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
    
@BP_Company.route("/get-by-id/<id_company>", methods=["GET"])
def get_company(id_company):
    company = session.query(Company).get(id_company)

    if(company is None):
        return jsonify({
            "mensaje": "No se encontro la compañia"
        }), 400
    
    return jsonify(company.to_dict()), 200

@BP_Company.route("/get-all", methods=["GET"])
def get_all_companies():
    companies = session.query(Company).all()

    if(companies is None):
        return jsonify({
            "mensaje": "No existe ninguna compañia registrada"
        }), 400
    # Convertir lista de objetos en lista de diccionarios
    companies_list = [company.to_dict() for company in companies]

    return jsonify(companies_list), 200


@BP_Company.route('/update-logo', methods=['PUT'])
def update_logo():
    # Validar si la imagen está presente
    if 'logo' not in request.files:
        return jsonify({"error": "El campo 'logo' es obligatorio"}), 400

    # Procesar la imagen
    if 'logo' in request.files:
        file = request.files['logo']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_nombre = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER")+"image/", nuevo_nombre)
        
        file.save(filepath)  # Guardar el archivo
    else:
        filepath = None

    company = Company(
        rfc=request.form.get("rfc"),
        logo=nuevo_nombre,
        nombre=request.form.get("nombre_empresa"),
        descripcion=request.form.get("descripcion"),
        facebook=request.form.get("facebook"),
        linkedIn=request.form.get("linkedIn"),
        link_x=request.form.get("link_x")
    )
    
    try:
        session.query(Company).filter(Company.id == 1).update(company)
        session.add_all([persona, company])
        session.commit()
        return jsonify({"mensaje": "¡Nuevo cliente registrado con éxito!"}), 200
    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({
            "error": "Llave duplicada. Esta persona ya existe."
        }), 400 

    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": "Error en la base de datos"
        }), 500
  