from flask import Blueprint, jsonify, request, send_file
from database.db import *
from models.Bandeja import Bandejas
from models.Dispositivos import Dispositivos
from models.Sensores_Log import Sensores_Log
from sqlalchemy import exc, func

BP_dispositivo = Blueprint('BP_dispositivo', __name__, url_prefix="/device")

@BP_dispositivo.route('/connect', methods=['POST'])
def connect_device():
    # Extrae los datos del ESP32 enviados en formato JSON
    mac_add = request.json.get("dir_mac")
    print(mac_add)

    if mac_add is None:
        return jsonify({"error": "Dirección MAC obligatoria"}), 400
        
    
    try:
        print("Sesión ABIERTA");
        session = Session()
        # Realizar la consulta
        disp = session.query(Dispositivos).filter_by(Wifi_MacAddress=mac_add).first()

        # Verificar si se obtuvo un resultado
        if disp is None:
            exist = session.query(Bandejas).filter_by(Wifi_MacAddress=mac_add).first()
            if exist:
                return jsonify({"error": "El dispositivo aun no ha sido registrado, sigue en la bandeja."}), 400
            newDisp = Bandejas()
            newDisp.Wifi_MacAddress = mac_add;
            newDisp.ip_client = request.remote_addr;
            session.add(newDisp)
            session.commit()

            return jsonify({"error": "Dispositivo no registrado. Ah sido puesto en la bandeja."}), 400

        session.query(Dispositivos).filter(Dispositivos.Wifi_MacAddress==mac_add).update({Dispositivos.last_connection: func.now()})
        session.commit()
        return jsonify({"mensaje": "¡Conexión establecida con éxito!", "rfc": disp.rfc_cli}), 200
    except exc.SQLAlchemyError as e:
        session.rollback()
        print(e.args)
        return jsonify({
            "error": (e.args)
        }), 400
    finally:
        session.close()  # Cerramos la sesión siempre
        print("Sesión Cerrada");

@BP_dispositivo.route("/send_data", methods=["POST"])
def send_data():
    required_fields = ["dir_mac", "presion", "caudal", "lit_con", "version"]
    missing_fields = [field for field in required_fields if not request.json.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    log = Sensores_Log(
        Wifi_MacAddress=request.json.get("dir_mac"),
        presion=request.json.get("presion"),
        caudal=request.json.get("caudal"),
        litros_consumidos=request.json.get("lit_con")
    )
    try:
        session.add(log)
        session.commit()
        #return jsonify({"message": "Registrado", "update": "New update"}), 200
        return jsonify({"message": "Registrado"}), 200
    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 
    
@BP_dispositivo.route("/await-confirm", methods=["POST"])
def await_confirm():
    session = Session()
    required_fields = ["macAdd"]
    missing_fields = [field for field in required_fields if not request.json.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    mac = request.json.get("macAdd");

    try:
        conReg = session.query(Dispositivos).get(mac)
        if conReg is None:
            return jsonify("Aun no se ha registrado"), 400
        
        return jsonify("Registrado"), 200
    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 
  

@BP_dispositivo.route('/download', methods=['GET'])
def download_file():
    # Ruta del archivo .bin dentro de la carpeta "public"
    file_path = os.path.join(os.getcwd(), 'public', 'Okox.ino.bin')
    
    # Verifica si el archivo existe
    if os.path.exists(file_path):
        # Envía el archivo .bin como respuesta
        return send_file(file_path, as_attachment=True, download_name="Okox.ino.bin")
    else:
        return "File not found", 404
    
