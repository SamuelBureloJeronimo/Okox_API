import re
import uuid
from sqlalchemy import desc, func
from flask_mail import Message
from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import create_access_token, decode_token, get_jwt, jwt_required
from werkzeug.utils import secure_filename

from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError

from config.middlewares import with_session
from database.db import *
from models.MyCompany import MyCompany
from models.Companies import Companies
from models.Posts import Posts
from models.Sessions import Sessions
from models.Usuarios import Usuarios
from models.address.Estados import Estados
from models.address.Municipios import Municipios
from models.address.Paises import Paises
from models.address.Colonias import Colonias

from config.mail_conf import mail

BP_Public = Blueprint('BP_Public', __name__)

@BP_Public.route('/init-dashboard', methods=["GET"])
@jwt_required()
@with_session
def init_dashboard(session):
        
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    email = jwt_data.get("email")  # "sub" es el campo "identity" por defecto
    id_company = jwt_data.get("id_company")  # Si guardaste "nombre" en el token

    user = session.query(Usuarios).filter_by(email=email).first();
    company = session.query(Companies).filter_by(rfc_user=id_company).first();
    okox = session.query(MyCompany).filter_by(rfc="BUJS030806UM7").first();

    if user is None or company is None:
        return jsonify({"email": email, "id": id_company}), 400

    data = {
        "email": user.email,
        "username": user.username,
        "img_user": user.imagen,
        "logo": company.logo,
        "nombre": company.nombre,
        "des": company.descripcion,
        "okox_logo": okox.logo
    }
    return jsonify(data), 200



@BP_Public.route("/enviar_usuario/<email>", methods=["POST"])
@jwt_required()
def enviar_usuario(email):
    # Expresión regular para validar el email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Validar el formato del email
    if not re.match(email_regex, email):
        return jsonify({"error": "El correo electrónico no tiene un formato válido"}), 400

    required_fields = ["username", "password"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    
    id_company = jwt_data.get("id_company")  # Si guardaste "nombre" en el token

    try:
        company = session.query(Companies).get(id_company)
        # Decodificar el token
        nombreComp = company.nombre
        username = request.form.get("username")
        password = request.form.get("password")
        url_login = "http://192.168.1.79:4200/login"

        # Cargar la plantilla y reemplazar valores
        with open("email_template.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        html_content = html_content.format(
            nombre_usuario=nombreComp,
            usuario=username,
            contraseña=password,
            url_login=url_login
        )

        msg = Message("Tu cuenta ha sido creada", recipients=[email])
        msg.html = html_content

        mail.send(msg)
        return jsonify("Correo enviado con éxito"), 200
    except ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401
    except DecodeError:
        return jsonify({"error": "Error al decodificar el token"}), 400


@BP_Public.route('/<path:filename>', methods=['GET'])
def public_files(filename):
    return send_from_directory('../public/', filename)

@BP_Public.route('/image/clients/<path:filename>', methods=['GET'])
def public_clients_files(filename):
    return send_from_directory('../public/image/clients', filename)

@BP_Public.route('/image/companies/<path:filename>', methods=['GET'])
def public_ccompanies_files(filename):
    return send_from_directory('../public/image/companies', filename)

@BP_Public.route('/login', methods=["POST"])
@with_session
def login(session):

    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    email = request.form.get("email");
    password = request.form.get("password");

    user = session.query(Usuarios).filter_by(email=email, password=password).first()    

    if user is None:
        user = session.query(Usuarios).filter_by(username=email, password=password).first()
        if user is None:
            return jsonify({"mensaje": "Correo o contraseña incorrecto"}), 401

    newSess = Sessions()
    newSess.rfc_user = user.rfc

    # Crea un token de acceso
    session.query(Usuarios).filter(Usuarios.rfc == user.rfc).update({ Usuarios.last_session: func.now()})
    session.add(newSess)
    session.commit()

    access_token = create_access_token(identity=str(user.rol), additional_claims={"email": user.email, "id_company": user.id_company, "rfc": user.rfc, "no_session": newSess.id})

    return jsonify({"token": access_token, "no_session": newSess.id})

@BP_Public.route('/auth-token', methods=['GET'])
@jwt_required()
def auth_token():
    # Obtener el token desde el encabezado o cuerpo de la solicitud
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401

    # Remover el prefijo "Bearer " si está presente
    if token.startswith("Bearer "):
        token = token.split("Bearer ")[1]

    try:
        # Decodificar el token
        decoded = decode_token(token)
        return jsonify(decoded), 200
    except ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401
    except DecodeError:
        return jsonify({"error": "Error al decodificar el token"}), 400


@BP_Public.route('/change-image-company', methods=['POST'])
@jwt_required()
@with_session
def change_image_company(session):
    
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    id_company = jwt_data.get("id_company")  # "sub" es el campo "identity" por defecto
    rol = jwt_data.get("sub")  # Si guardaste "nombre" en el token
    
    if(rol == "4"):
        return jsonify("No tienes permisos de administrador"), 401
    
    # Validar si la imagen está presente
    if 'img' not in request.files:
        return jsonify({"error": "El campo 'img' es obligatorio"}), 400
    
    # Procesar la imagen
    file = request.files['img']
    company = session.query(Companies).filter_by(rfc_user=id_company).first()
    if company.logo == "default_perfil.png":
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_nombre = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER")+"image/companies/", nuevo_nombre)
        file.save(filepath)
        session.query(Companies).filter(Companies.logo == id_company).update({Companies.logo: nuevo_nombre})
        session.commit()
    else:
        file.save("public/image/companies/"+company.logo)
    
    return jsonify("¡Imagen actualizada con éxito!"), 200
        
@BP_Public.route('/change-image-profile', methods=['POST'])
@jwt_required()
@with_session
def change_image_perfil(session):
    
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    
    email = jwt_data.get("email")  # "sub" es el campo "identity" por defecto
    
    # Validar si la imagen está presente
    if 'img' not in request.files:
        return jsonify({"error": "El campo 'img' es obligatorio"}), 400
    
    # Procesar la imagen
    file = request.files['img']
    user = session.query(Usuarios).filter_by(email=email).first()
    if user.imagen == "/clients/default_perfil.png":
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_nombre = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER")+"image/clients/", nuevo_nombre)
        file.save(filepath)
        session.query(Usuarios).filter(Usuarios.email == email).update({Usuarios.imagen: "/image/clients/"+nuevo_nombre})
        session.commit()
    else:
        file.save("public/image"+user.imagen)
    
    return jsonify("¡Imagen actualizada con éxito!"), 200
         

@BP_Public.route('/get-posts', methods=['GET'])
@with_session
def get_all_posts(session):
    posts = session.query(Posts).order_by(desc(Posts.fech_alta)).all();

    # Convertir lista de objetos en lista de diccionarios
    posts_list = [pais.to_dict() for pais in posts]

    return jsonify(posts_list), 200



@BP_Public.route('/get-paises', methods=['GET'])
@with_session
def get_paises(session):

    paises = session.query(Paises).all();
    if(paises is None):
        return jsonify({
            "mensaje": "No se encontro paises"
        }), 400

    # Convertir lista de objetos en lista de diccionarios
    paises_list = [pais.to_dict() for pais in paises]
    
    return jsonify(paises_list), 200

@BP_Public.route('/get-estados/<id_pais>', methods=['GET'])
@with_session
def get_estados(session, id_pais):

    estados = session.query(Estados).filter_by(pais_id=id_pais).all();
        
    if(estados is None):
        return jsonify({
        "mensaje": "No se encontro paises"
        }), 400

    # Convertir lista de objetos en lista de diccionarios
    estados_list = [est.to_dict() for est in estados]

    return jsonify(estados_list), 200

@BP_Public.route('/get-municipios/<id_estado>', methods=['GET'])
@with_session
def get_municipios(session, id_estado):

    mun = session.query(Municipios).filter_by(est_id=id_estado).all();
    
    if(mun is None):
        return jsonify({
        "mensaje": "No se encontro Municipios"
        }), 400

    # Convertir lista de objetos en lista de diccionarios
    municipios_list = [m.to_dict() for m in mun]

    return jsonify(municipios_list), 200

@BP_Public.route('/get-colonias/<id_municipio>', methods=['GET'])
@with_session
def get_colonias(session, id_municipio):

    colns = session.query(Colonias).filter_by(mun_id=id_municipio).all();

    if(colns is None):
        return jsonify({
        "mensaje": "No se encontro Colonias"
        }), 400

    # Convertir lista de objetos en lista de diccionarios
    colonias_list = [col.to_dict() for col in colns]

    return jsonify(colonias_list), 200

@BP_Public.route('/get-colonias-by-cp/<cp>', methods=['GET'])
@with_session
def get_colonias_by_cp(session, cp):

    colns = session.query(Colonias).filter_by(cp=cp).all();

    if(colns is None):
        return jsonify({
        "mensaje": "No se encontro Colonias"
        }), 400

    # Convertir lista de objetos en lista de diccionarios
    colonias_list = [col.to_dict() for col in colns]

    return jsonify(colonias_list), 200
        
