from flask import Flask, request, jsonify
import mysql.connector, datetime, urllib.parse
from mysql.connector import Error
LIMIT_LH = 6.0

app = Flask(__name__)
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
# QUERY's - CLIENTES
@app.route('/registrar-cliente', methods=['POST'])
@app.route('/actualizar-cliente/<id_cliente>', methods=['PUT'])
@app.route('/obtener-all-clientes', methods=['GET'])
#QUERY's - PERSONAS
@app.route('/registrar-persona', methods=['POST'])
@app.route('/obtener-persona/<id_persona>', methods=['GET'])
@app.route('/obtener-all-personas', methods=['GET'])
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
@app.route('/registrar-dispostivo', methods=['POST'])
@app.route('/obtener-dispostivo/<id_dispositivo>', methods=['GET'])
@app.route('/obtener-all-dispostivo', methods=['GET'])
@app.route('/actualizar-dispostivo/<id_dispostivo>', methods=['PUT'])
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

        return jsonify({"res": "Datos obtenidos correctamente", "id_cliente": res1[0], "volumen_Litros": res1[1]}), 200
    except Error as e:
        print("Error al insertar datos", e)
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
        return jsonify({"res": "Tu consumo a superado los "+str(LIMIT_LH)+"L por hora", "cod": 101}), 201

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
        return jsonify({"status": "Datos guardados correctamente", "cod": 111}), 201
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