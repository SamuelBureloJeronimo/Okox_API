from random import randint
import uuid
from flask import Blueprint, request, jsonify
from database.db import *
from sqlalchemy import exc
from werkzeug.utils import secure_filename

import os

from models.Companies import Companies
from models.Personas import Personas
from models.Usuarios import Usuarios

# Cargar variables desde el archivo .env
load_dotenv()

BP_System = Blueprint('BP_System', __name__, url_prefix='/api/v1/')

@BP_System.route('/create', methods=['POST'])
def create_owner():
    required_fields = ["rfc", "nombre", "app", "apm", "fech_nac", "sex", "tel", "tel_empr","id_colonia", "nombre_empr", "descripcion", "col_empr"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

    # Validar si la imagen está presente
    if 'logo' not in request.files:
        return jsonify({"error": "El campo 'logo' es obligatorio"}), 400
    
    # Procesar la imagen
    if 'logo' in request.files:
        file = request.files['logo']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_nombre = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER")+"image/companies/", nuevo_nombre)
        
        file.save(filepath)  # Guardar el archivo
    else:
        filepath = None

    persona = Personas()
    persona.rfc=request.form.get("rfc"),
    persona.nombre=request.form.get("nombre"),
    persona.app=request.form.get("app"),
    persona.apm=request.form.get("apm"),
    persona.fech_nac=request.form.get("fech_nac"),
    persona.sex=request.form.get("sex"),
    persona.tel=request.form.get("tel"),
    persona.id_colonia=request.form.get("id_colonia")

    company = Companies()
    company.rfc_user=request.form.get("rfc"),
    company.logo="/companies/"+nuevo_nombre,
    company.nombre=request.form.get("nombre_empr"),
    company.descripcion=request.form.get("descripcion"),
    company.telefono=request.form.get("tel_empr"),
    company.facebook=request.form.get("facebook"),
    company.linkedIn=request.form.get("linkedIn"),
    company.link_x=request.form.get("link_x")
    company.id_colonia=request.form.get("col_empr")

    user = Usuarios()
    user.rfc=request.form.get("rfc"),
    user.username=request.form.get("username"),
    user.password=request.form.get("password"),
    user.email=request.form.get("email"),
    user.rol=4
    user.id_company=company.rfc_user
    
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
    
@BP_System.route("/get-by-id/<id_company>", methods=["GET"])
def get_company(id_company):
    company = session.query(Companies).get(id_company)

    if(company is None):
        return jsonify({
            "mensaje": "No se encontro la compañia"
        }), 400
    
    return jsonify(company.to_dict()), 200

@BP_System.route("/get-all", methods=["GET"])
def get_all_companies():
    companies = session.query(Companies).all()

    if(companies is None):
        return jsonify({
            "mensaje": "No existe ninguna compañia registrada"
        }), 400
    # Convertir lista de objetos en lista de diccionarios
    companies_list = [company.to_dict() for company in companies]

    return jsonify(companies_list), 200
