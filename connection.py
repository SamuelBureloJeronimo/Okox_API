from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# LR:9Ia~f4U

# Configuración de la conexión a la base de datos MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Cambia esto por la dirección de tu servidor MySQL
            user="root",
            password="",
            database="prueba_esp"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error al conectar a la base de datos", e)
        return None

# Endpoint para recibir datos
@app.route('/datos', methods=['POST'])
def recibir_datos():
    # Extrae los datos del ESP32 enviados en formato JSON
    data = request.json
    sensor_value = data.get('sensor_value')
    
    if sensor_value is None:
        return jsonify({"error": "Datos no válidos"}), 400

    # Conectar a la base de datos
    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    # Insertar datos en la base de datos
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO datos_esp32 (sensor_value) VALUES (%s)"
        cursor.execute(insert_query, (sensor_value,))
        connection.commit()
        cursor.close()
        return jsonify({"status": "Datos guardados correctamente"}), 201
    except Error as e:
        print("Error al insertar datos", e)
        return jsonify({"error": "Error al guardar datos"}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
