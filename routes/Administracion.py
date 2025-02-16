from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from database.db import *
from models.Company import Company
from models.Usuarios import Usuarios


BP_Administracion = Blueprint('BP_Administracion', __name__, url_prefix='/admin')

@BP_Administracion.route('/init-dashboard', methods=["GET"])
@jwt_required()
def init_dash():
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