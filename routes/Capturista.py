import secrets
import string
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from database.db import *
from sqlalchemy import exc
from models.Clientes import Clientes
from models.Company import Company
from models.Personas import Personas
from models.Usuarios import Usuarios
from models.Umbral_Clientes import Umbral_Clientes


BP_Capturista = Blueprint('BP_Capturista', __name__, url_prefix='/capturista')

@BP_Capturista.route('/create-cliente', methods=['POST'])
@jwt_required()
def create_client():
    required_fields = ["rfc", "nombre", "app", "apm", "fech_nac", "sex", "id_colonia", "id_umbral", "tel"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    id_company = jwt_data.get("id_company")  # Si guardaste "nombre" en el token
    
    persona = Personas(
        rfc=request.form.get("rfc"),
        nombre=request.form.get("nombre"),
        app=request.form.get("app"),
        apm=request.form.get("apm"),
        fech_nac=request.form.get("fech_nac"),
        tel=request.form.get("tel"),
        sex=request.form.get("sex"),
        id_colonia=request.form.get("id_colonia")
    )

    user = Usuarios(
        rfc=request.form.get("rfc"),
        email=request.form.get("email"),
        username="username_"+persona.rfc,
        password=gn_pass(7),
        id_company=id_company
    )

    cliente = Clientes(
        rfc=request.form.get("rfc"),
        id_umbral=request.form.get("id_umbral"),
        id_company=id_company
    )

    try:
        session.add(persona)
        session.add(cliente)
        session.add(user)
        session.add_all([persona, cliente, user])
        session.commit()
        return jsonify({"mensaje": "¡Nuevo cliente registrado con éxito!", "username": user.username, "password": user.password}), 200
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

@BP_Capturista.route('/init-dashboard', methods=["GET"])
@jwt_required()
def init_dash_cp():
    
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    
    email = jwt_data.get("sub")  # "sub" es el campo "identity" por defecto
    id_company = jwt_data.get("id_company")  # Si guardaste "nombre" en el token

    
    user = session.query(Usuarios).filter_by(email=email).first();
    company = session.query(Company).filter_by(id=id_company).first();


    if user is None or company is None:
        return jsonify({"email": email, "id": id_company}), 400


    data = {
        "email": user.email,
        "username": user.username,
        "img_user": user.imagen,
        "logo": company.logo,
        "nombre": company.nombre,
    }
    return jsonify(data), 200

@BP_Capturista.route('/get-umbrales', methods=["GET"])
@jwt_required()
def get_umbrales():
    try:        
        with Session() as session:
            umbrales = session.query(Umbral_Clientes).all();
            if(umbrales is None):
                return jsonify({
                    "mensaje": "No se encontro Umbrales"
                }), 400
        
            # Convertir lista de objetos en lista de diccionarios
            umb_list = [um.to_dict() for um in umbrales]
            
            return jsonify(umb_list), 200

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

def gn_pass(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))