from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory

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

from routes.Dispositivo_routes import BP_dispositivo
from routes.Company_routes import BP_Company
from routes.Cliente_routes import BP_Clientes

# Cargar variables desde el archivo .env
load_dotenv()

if not os.path.exists(os.getenv("UPLOAD_FOLDER")):
    os.makedirs(os.getenv("UPLOAD_FOLDER"))

app = Flask(__name__)
app.register_blueprint(BP_dispositivo)
app.register_blueprint(BP_Company)
app.register_blueprint(BP_Clientes)

# Habilitar CORS para todos los orígenes y rutas
CORS(app)

@app.route('/image/<path:filename>')
def public_files(filename):
    return send_from_directory('public/image', filename)

@app.route('/login', methods=["GET"])
def login():
    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    email = request.form.get("email");
    password = request.form.get("password");

    user = session.query(Usuarios).filter_by(email=email, password=password).first()

    if user is None:
        return jsonify({"mensaje": "Correo o contraseña incorrecto"})

    return jsonify(user.to_dict())

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000, debug=True)