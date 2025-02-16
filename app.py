from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, decode_token, jwt_required, get_jwt_identity
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError
from sqlalchemy import func
from flask_mail import Mail, Message
from database.db import *

import os

from models.Personas import Personas
from models.Usuarios import Usuarios


# Modelos para el administrador
from models.Company import Company
from models.Motivo_Suspensiones import Motivo_Suspensiones
from models.Suspensiones import Suspensiones
from models.Mantenimientos import Mantenimientos

# Modelos para el técnico

# Modelos para el capturista
from models.address.Paises import Paises
from models.address.Municipios import Municipios
from models.address.Estados import Estados
from models.address.Colonias import Colonias

# Modelos para el cliente
from models.Clientes import Clientes
from models.Reportes_Fugas import Reportes_Fugas
from models.Sensores_Log import Sensores_Log
from models.Pagos import Pagos
from models.Dispositivos import Dispositivos
from models.Notificaciones import Notificaciones
from models.Umbral_Clientes import Umbral_Clientes
from models.Contrato import Contratos

from routes.Dispositivo_routes import BP_dispositivo
from routes.Company_routes import BP_Company
from routes.Cliente_routes import BP_Clientes
from routes.Administracion import BP_Administracion
from routes.Address import BP_Address
from routes.Usuarios import BP_Usuarios
from routes.Capturista import BP_Capturista

# Cargar variables desde el archivo .env
load_dotenv()

if not os.path.exists(os.getenv("UPLOAD_FOLDER")):
    os.makedirs(os.getenv("UPLOAD_FOLDER"))

app = Flask(__name__)
app.register_blueprint(BP_dispositivo)
app.register_blueprint(BP_Company)
app.register_blueprint(BP_Clientes)
app.register_blueprint(BP_Administracion)
app.register_blueprint(BP_Address)
app.register_blueprint(BP_Usuarios)
app.register_blueprint(BP_Capturista)
# Configuración de la clave secreta para JWT
app.config["JWT_SECRET_KEY"] = "LLAVE-ULTRA-SECRETA"  # Cambia esto en producción
jwt = JWTManager(app)

# Configuración del servidor SMTP
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "santorosario0608@gmail.com" #Es el correo electrónico del remitente (el que envía el correo).
app.config["MAIL_PASSWORD"] = "lnlj hdqs yjkv rpzp" #Es la contraseña que se usa para autenticarse en el servidor SMTP.
app.config["MAIL_DEFAULT_SENDER"] = ("Okox Service", "santorosario0608@gmail.com") #Define el correo que aparecerá como remitente en los emails.

mail = Mail(app)

# Habilitar CORS para todos los orígenes y rutas
CORS(app)

@app.route("/enviar_usuario/<email>", methods=["POST"])
def enviar_usuario(email):
    nombreComp = request.form.get("nombreComp")
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
    return "Correo enviado con éxito"

@app.route('/image/<path:filename>')
def public_files(filename):
    return send_from_directory('public/image', filename)

@app.route('/login', methods=["POST"])
def login():

    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    email = request.form.get("email");
    password = request.form.get("password");

    with Session() as session:
        user = session.query(Usuarios).filter_by(email=email, password=password).first()

        if user is None:
            return jsonify({"mensaje": "Correo o contraseña incorrecto"}), 401

        # Crea un token de acceso
        access_token = create_access_token(identity=email, additional_claims={"role": user.rol, "id_company": user.id_company})

        session.query(Usuarios).filter(Usuarios.rfc == user.rfc).update({ Usuarios.token: access_token, Usuarios.last_session: func.now()})
        session.commit()

        return jsonify({"user": user.to_dict(), "token": access_token})

@app.route('/auth-token', methods=['GET'])
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
        return jsonify({"message": "Token válido", "rol": decoded["role"]}), 200
    except ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401
    except DecodeError:
        return jsonify({"error": "Error al decodificar el token"}), 400


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000, debug=True)