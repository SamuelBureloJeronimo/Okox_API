import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from database.db import *
from sqlalchemy import exc
from werkzeug.utils import secure_filename

from models.Companies import Companies
from models.Personas import Personas
from models.Reportes_Fugas import Reportes_Fugas
from models.Usuarios import Usuarios

BP_Clientes = Blueprint('BP_Clientes', __name__, url_prefix='/clientes')

@BP_Clientes.route("/upload-report", methods=["POST"])
@jwt_required()
def upload_report():
    required_fields = ["razon", "id_col"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

        # Validar si la imagen está presente
    if 'image' not in request.files:
        return jsonify({"error": "El campo 'image' es obligatorio"}), 400
    
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    rfc = jwt_data.get("rfc")  # Si guardaste "nombre" en el token

        # Procesar la imagen
    if 'image' in request.files:
        file = request.files['image']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_nombre = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER")+"image/reportes/", nuevo_nombre)
        
        file.save(filepath)  # Guardar el archivo
    else:
        filepath = None
    
    report = Reportes_Fugas(
        rfc_cli=rfc,
        foto="/reportes/"+nuevo_nombre,
        razon=request.form.get("razon"),
        id_colonia=request.form.get("id_col")
    )
    
    try:
        session.add(report)
        session.commit()
        return jsonify({"mensaje": "¡Nuevo reporte registrado con éxito!"}), 200
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
    
@BP_Clientes.route("/get-all-reports", methods=["GET"])
@jwt_required()
def get_all_reports():
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    
    rfc = jwt_data.get("rfc")

    try:
        report = session.query(Reportes_Fugas).filter_by(rfc_cli=rfc).all()
        # Convertir lista de objetos en lista de diccionarios
        report_list = [rep.to_dict() for rep in report]
        return jsonify(report_list), 200
    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 