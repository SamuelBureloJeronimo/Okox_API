from datetime import datetime
from flask_cors import CORS
from flask import Flask, jsonify, send_file
import os

import urllib

from database.db import *

from models.Personas import Personas
from models.Usuarios import Usuarios

# Modelos para el administrador
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

app = Flask(__name__)
# Habilitar CORS para todos los orígenes y rutas
CORS(app)

@app.route('/download', methods=['GET'])
def download_file():
    # Ruta del archivo .bin dentro de la carpeta "public"
    file_path = os.path.join(os.getcwd(), 'public', 'Okox.ino.bin')
    
    # Verifica si el archivo existe
    if os.path.exists(file_path):
        # Envía el archivo .bin como respuesta
        return send_file(file_path, as_attachment=True, download_name="Okox.ino.bin")
    else:
        return "File not found", 404

# ============== IoT y Servidor ============== #
# Se obtienen los datos iniciales: id_cliente y volumen_Litros
@app.route('/init_device/<codedMac>', methods=['GET'])
def initialitation(codedMac):

    # Extrae los datos del ESP32 enviados en formato JSON
    # Decodificar la URL
    # decodedMAC = urllib.parse.unquote(codedMac)
    decodedMAC = codedMac

    if decodedMAC is None:
        return jsonify({"error": "Datos no válidos"}), 400
    
    # Suponiendo que 'engine' es tu motor de SQLAlchemy
    session = Session()

    # Realizar la consulta
    disp = session.query(Dispositivos).all()

    # Verificar si se obtuvo un resultado
    if disp is None:
        print({"error": "El dispositivo no está registrado."})
    else:
        return jsonify({"dispositivos registrados": disp}), 200


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000)