from flask import Flask, request, jsonify
import mysql.connector, datetime, urllib.parse
from mysql.connector import Error
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
LIMIT_LH = 26.0

app = Flask(__name__)

# Configura una clave secreta para firmar los tokens
app.config["JWT_SECRET_KEY"] = "CLAVE-ULTRA-SECRETA"

# Inicializa el manejador de JWT
jwt = JWTManager(app)
# ======= CONSULTAS PARA LOS USUARIOS ====== #
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "usuario" or password != "contraseña":
        return jsonify({"msg": "Credenciales incorrectas"}), 401

    # Crea un token de acceso
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# ======== CONSULTAS SOLO PARA CLIENTES REGISTRADOS ======== #
# QUERY's - CLIENTES
@app.route('/obtener-cliente/<id_cliente>', methods=['GET'])
# QUERY's - REPORTES
@app.route('/crear-reporte/<id_cliente>', methods=['POST'])
@app.route('/obtener-all-reportes-by-client/<id_cliente>', methods=['GET'])
@app.route('/obtener-reporte/<id_cliente>/<id_reporte>', methods=['GET'])
#QUERY's - PERSONAS
@app.route('/obtener-persona/<id_cliente>/<id_persona>', methods=['GET'])

# ============== RESERVADO PARA ADMINISTRADORES ============== #
# QUERY's - REPORTES
@app.route('/obtener-all-reportes', methods=['GET'])
@app.route('/obtener-reporte/<id_reporte>', methods=['GET'])
@app.route('/update-reporte/<id_reporte>', methods=['PUT'])
# Query's - SUSPENSIÓN
@app.route('/registrar-suspension/<id_cliente>', methods=['POST'])
@app.route('/obtener-suspension-by-client/<id_cliente>', methods=['GET'])
@app.route('/obtener-all-suspension', methods=['GET'])
@app.route('/actualizar-suspension/<id_cliente>', methods=['PUT'])
# Query's - INCIDENTES
@app.route('/registrar-incidente', methods=['POST'])
@app.route('/actualizar-incidente', methods=['PUT'])
@app.route('/obtener-incidente/<id_incidente>', methods=['GET'])
@app.route('/obtener-all-incidentes', methods=['GET'])
# Query's - ADMINISTRADORES
@app.route('/registrar-admin', methods=['POST'])
@app.route('/obtener-admin/<id_admin>', methods=['GET'])
@app.route('/obtener-all-admin', methods=['GET'])
@app.route('/eliminar-admin', methods=['DELETE'])
# Query's - AVISOS
@app.route('/registrar-aviso', methods=['POST'])
@app.route('/obtener-aviso/<id_aviso>', methods=['GET'])
@app.route('/obtener-all-avisos', methods=['GET'])
@app.route('/actualizar-aviso/<id_aviso>', methods=['PUT'])
# Query's - DISPOSITIVOS
@app.route('/obtener-dispostivo/<id_dispositivo>', methods=['GET'])
@app.route('/obtener-all-dispostivo', methods=['GET'])
@app.route('/actualizar-dispostivo/<id_dispostivo>', methods=['PUT'])

# ============== RESERVADO PARA CAPTURISTAS Y ADMINISTRADORES ============== #
# Query's - CLIENTES
@app.route('/obtener-all-clientes', methods=['GET'])
@app.route('/registrar-cliente', methods=['POST'])
def registrar_cliente():
    # Primero se debe registrar una persona
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    
    # Despues un cliente

    # Al final se crea su usuario

    #Se genera su Token
@app.route('/actualizar-cliente/<id_cliente>', methods=['PUT'])

# ============== RESERVADO PARA TÉCNICOS ============== #


# ============== IoT y Servidor ============== #
# Se obtienen los datos iniciales: id_cliente y volumen_Litros
@app.route('/initialitation/<codedMac>', methods=['GET'])
def initialitation(codedMac):
    hora_actual = datetime.datetime.now()
    fecha = str(hora_actual.year)+"-"+str(hora_actual.month)+"-"+str(hora_actual.day)

    # Extrae los datos del ESP32 enviados en formato JSON
    # Decodificar la URL
    decodedMAC = urllib.parse.unquote(codedMac)

    if decodedMAC is None:
        return jsonify({"error": "Datos no válidos"}), 400
    
    # Conectar a la base de datos
    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    # Consultar datos en la base de datos
    try:
        total = 0
        cursor = connection.cursor()        
        query_2 = "SELECT dispositivos.id_dispositivo, cliente.id_cliente FROM cliente JOIN dispositivos ON dispositivos.Wifi_MacAddress=\""+str(decodedMAC)+"\";"
        cursor.execute(query_2)
        # Obtener el resultado
        res1 = cursor.fetchone()
        
        # Verificar si se obtuvo un resultado
        if res1 is None:
            return jsonify({"error": "El dispositivo no esta registrado."}), 500
        
        query_3 = "SELECT id_cliente, SUM(presion) FROM presion WHERE id_cliente=%s AND fecha BETWEEN %s AND %s;"
        params = (str(res1[1]), fecha+" 00:00:00", fecha+" 23:59:59")
        cursor.execute(query_3, params)

        # Obtener el resultado
        res1 = cursor.fetchone()

        return jsonify({"res": "Datos obtenidos correctamente", "id_cliente": res1[0], "volumen_Litros": res1[1]/60}), 200
    except Error as e:
        print("Error al consultar los datos", e)
        return jsonify({"error": "Error al consultar los datos"}), 500
    finally:
        connection.close()

# Envía datos de los sensores a la base de datos
@app.route('/presion', methods=['POST'])
def recibir_datos():
    # Extrae los datos del ESP32 enviados en formato JSON
    data = request.json
    presion = data.get('presion')
    id_cliente = data.get('id_cliente')
    volumen_Litros = data.get('volumen_Litros')
    
    if (presion is None) or (id_cliente is None) or (volumen_Litros is None):
        return jsonify({"error": "Datos no válidos"}), 400
    
    if float(volumen_Litros) > LIMIT_LH:
        return jsonify({"res": "Tu consumo a superado los "+str(LIMIT_LH)+"L por hora"}), 200

    # Conectar a la base de datos
    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    # Insertar datos en la base de datos
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO presion (presion,id_cliente) VALUES ("+presion+","+id_cliente+")"
        cursor.execute(insert_query)
        connection.commit()
        cursor.close()
        return jsonify({"status": "Datos guardados correctamente"}), 200
    except Error as e:
        print("Error al insertar datos", e)
        return jsonify({"error": "Error al guardar datos"}), 500
    finally:
        connection.close()


# Configuración de la conexión a la base de datos MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="srv1601.hstgr.io",  # Cambia esto por la dirección de tu servidor MySQL
            user="u839116441_admin",
            password="VepZHycV~p3:",
            database="u839116441_sgirap"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error al conectar a la base de datos", e)
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)