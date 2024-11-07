from flask import Flask, request, jsonify
import mysql.connector, datetime
from mysql.connector import Error

LIMIT_LH = 6.0

app = Flask(__name__)

# LR:9Ia~f4U

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
@app.route('/get_fct')
def get_fct():
    hora_actual = datetime.datetime.now()
    fecha = str(hora_actual.year)+"-"+str(hora_actual.month)+"-"+str(hora_actual.day)

    # Extrae los datos del ESP32 enviados en formato JSON
    data = request.json
    id_cliente = data.get('id_cliente')

    if id_cliente is None:
        return jsonify({"error": "Datos no válidos"}), 400
    
    # Conectar a la base de datos
    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    # Consultar datos en la base de datos
    try:
        total = 0
        cursor = connection.cursor()        
        query_1 = "SELECT id_cliente, SUM(presion) FROM presion WHERE id_cliente="+str(id_cliente)+";"
        cursor.execute(query_1)
        # Obtener el resultado
        resultado = cursor.fetchone()
        
        # Verificar si se obtuvo un resultado
        if resultado:
            total = resultado[1]/60
            print(f"Cliente ID: {resultado[0]}, Consumo Total: {total}")
        else:
            print("No se encontraron registros para el cliente especificado.")
        
        return jsonify({"res": "Datos obtenidos correctamente", "cod": 201, "total": total}), 201
    except Error as e:
        print("Error al insertar datos", e)
        return jsonify({"error": "Error al consultar los datos"}), 500
    finally:
        connection.close()


# Endpoint para recibir datos
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)