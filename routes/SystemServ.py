from datetime import datetime, timedelta
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt
import jwt
from database.db import *
from sqlalchemy import Date, case, cast, desc, exc, func
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import os

from index import with_session
from models.Companies import Companies
from models.Personas import Personas
from models.Sessions import Sessions
from models.Usuarios import Usuarios
from models.Visitas import Visitas

# Cargar variables desde el archivo .env
load_dotenv()

BP_System = Blueprint('BP_System', __name__, url_prefix='/api/v1/')

@BP_System.route('/create', methods=['POST'])
@with_session
def create_owner(session):
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
    
    session.add_all([persona, company, user])
    session.commit()
    return jsonify({"mensaje": "¡Nueva compañia registrada con éxito!"}), 200

    
@BP_System.route("/get-by-id/<id_company>", methods=["GET"])
@with_session
def get_company(session, id_company):
    company = session.query(Companies).get(id_company)

    if(company is None):
        return jsonify({
            "mensaje": "No se encontro la compañia"
        }), 400
    
    return jsonify(company.to_dict()), 200

@BP_System.route("/get-all", methods=["GET"])
@with_session
def get_all_companies(session):
    companies = session.query(Companies).all()

    if(companies is None):
        return jsonify({
            "mensaje": "No existe ninguna compañia registrada"
        }), 400
    # Convertir lista de objetos en lista de diccionarios
    companies_list = [company.to_dict() for company in companies]

    return jsonify(companies_list), 200

@BP_System.route("/visit", methods=["POST"])
def visit():
    session = Session()
    required_fields = ["t-carga", "ip", "t-page", "userAgent", "url"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

    tiempo_carga = request.form.get('t-carga')

    # Verificar si es un número válido o convertirlo al tipo adecuado
    try:
        tiempo_carga = float(tiempo_carga)
    except ValueError:
        tiempo_carga = None  # O el valor que desees en caso de error (o un valor por defecto)
    
    if request.form.get("url") == "/":
        url = "/home"
    else:
        url = request.form.get("url")

    newVis = Visitas(
        url=url,
        ip_user=request.form.get("ip"),
        tiempo_carga=request.form.get("t-carga"),
        duracion=request.form.get("t-page"),
        origin=request.form.get("userAgent")
    )

    try:
        if(request.form.get("token") != ""):
            payload = jwt.decode(request.form.get("token"), "LLAVE-ULTRA-SECRETA", algorithms=["HS256"])
            newVis.rfc_user = payload.get("rfc")
            newVis.id_session = payload.get("no_session")
            
        session.add(newVis)
        session.commit()
        return jsonify({'message': 'Visita registrada exitosamente'}), 200
    except IntegrityError as e:
        session.rollback()
        return jsonify({"error": "Error de integridad en la base de datos.", "detalle": str(e)}), 400
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Error en la base de datos.", "detalle": str(e)}), 500
    finally:
            session.close()  # Cerramos la sesión siempre
            print("Sesión Cerrada");


@BP_System.route("/get-metrics", methods=["GET"])
@with_session
def get_metrics(session):
    # Obtener fecha de hoy
    today = datetime.now().date()

    # 1 **Visitas de hoy**
    visitas_hoy = session.query(Visitas).filter(func.date(Visitas.fecha) == today).count()

    # 2 **Usuarios únicos de hoy (IP únicas)**
    us_un = session.query(func.count(func.distinct(Visitas.ip_user))).filter(
    func.date(Visitas.fecha) == today).scalar()


    total_visitas = session.query(Visitas).count()

    # 3 **Tasa de rebote**
    rebotes = session.query(Visitas).filter(Visitas.duracion < 5).count()
    t_reb = (rebotes / total_visitas) * 100 if total_visitas > 0 else 0

    # 4 **Tasa de retención**
    ret = session.query(Visitas).filter(Visitas.duracion >= 5).count()
    t_ret = (ret / total_visitas) * 100 if total_visitas > 0 else 0


    # Obtener las 3 páginas más visitadas
    paginas_mas_visitadas = (
        session.query(Visitas.url, func.count().label("visitas"))
        .group_by(Visitas.url)
        .order_by(desc("visitas"))
        .limit(6)
        .all()
    )

    tasa = {
        "visitas_hoy": visitas_hoy,
        "us_un": us_un,
        "t_reb": round(t_reb, 0),
        "t_ret": round(t_ret, 0)
    }

    # Contar las visitas por dispositivo
    visitas_por_dispositivo = (
        session.query(
            case(
                (Visitas.origin.ilike("%mobile%"), "mobile"),
                (Visitas.origin.ilike("%tablet%"), "tablet"),
                else_="desktop"
            ).label("dispositivo"),
            func.count().label("total")
        )
        .group_by("dispositivo")
        .all()
    )

    # Formatear respuesta
    resultado = {
        "top_paginas": [{"url": url, "visitas": visitas} for url, visitas in paginas_mas_visitadas],
        "visitas_por_dispositivo": {dispositivo: total for dispositivo, total in visitas_por_dispositivo},
        "tasa": tasa
    }

    return jsonify(resultado)