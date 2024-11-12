import secrets
import string
from flask import Flask, request, jsonify
import datetime, urllib.parse
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity
from flask_cors import CORS

from connection import connect_to_database
from mysql.connector import Error

from Models.Usuario import Usuario
from Models.Cliente import Cliente
from Models.Persona import Persona

LIMIT_LH = 6.0

app = Flask(__name__)
# Habilitar CORS para todos los orígenes y rutas
CORS(app)

# Configura una clave secreta para firmar los tokens
app.config["JWT_SECRET_KEY"] = "CLAVE-ULTRA-SECRETA"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=0.5)  # El token expira en 1 hora

# Inicializa el manejador de JWT
jwt = JWTManager(app)
# ======= CONSULTAS PARA LOS USUARIOS ====== #
@app.route("/login", methods=["POST"])
def login():
    # Consultar datos en la base de datos
    try:
        username = request.json.get("username")
        password = request.json.get("password")

        # Conectar a la base de datos
        connection = connect_to_database()
        if connection is None:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    
        cursor = connection.cursor()
        print("Conexión a la base de datos ABIERTA.") 

        query = "SELECT * FROM usuarios WHERE username=%s AND password=%s;"
        cursor.execute(query, (username, password))

        # Obtener el resultado
        res1 = cursor.fetchone()

        if res1 == None:
            return jsonify({"message": "Credenciales invalidas"}), 400
        elif res1[2] != username or res1[3] != password:
            return jsonify({"message": "Credenciales invalidas"}), 400

        # Crea un token de acceso
        access_token = create_access_token(identity=username, additional_claims={"role": res1[4]})


        query2 = "UPDATE usuarios SET token=%s, last_session=%s WHERE id=%s;"
        cursor.execute(query2, (access_token, datetime.datetime.now(), res1[0]))

        # Verifica si se actualizó correctamente
        if cursor.rowcount == 0:
            return jsonify({"error": "Error al guardar los datos, ningún registro afectado"}), 500
        
        # Cerrar la conexión
        connection.commit()
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"access_token": access_token}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")


# ======== CONSULTAS SOLO PARA CLIENTES REGISTRADOS ======== #
# QUERY's - CLIENTES
@app.route('/obtener-data-cliente/<id_cliente>', methods=['GET'])
#@jwt_required()
def get_data_client(id_cliente):

    '''
    # Obtener el rol desde los claims del JWT
    claims = get_jwt()  # Obtener la identidad (username) del token
    role = claims.get("role")

    # Verificar que el usuario tiene el rol de administrador o Capturista
    if role == 1 or role == 3: # 0 == Cliente, 2 == Técnico
        return jsonify({"mensaje":"No tienes autorizado el acceso."}), 403
    
    '''
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
        
        ######################################################################
        # Cliente
        # [id_persona], [id_dispositivo], estado_servicio, fecha_contratacion
        # Persona -> WHERE id=id_persona
        # nombre, app, apm, fech_nac, sex, [id_colonia]
        # Colonia -> WHERE id=id_colonia
        # nombre, asentamiento, ciudad, codigo_postal
        # Usuario -> WHERE id_persona=id_persona
        # id, username, rol, last_session

        insert_query = '''
        SELECT
            clientes.id,
            clientes.estado_servicio,
            clientes.fecha_contratacion,
            personas.nombre,
            personas.app,
            personas.apm,
            personas.fech_nac,
            personas.sex,
            dispositivos.Wifi_MacAddress,
            colonias.nombre AS colonia_nombre,
            colonias.asentamiento,
            colonias.ciudad,
            colonias.codigo_postal,
            usuarios.id AS usuario_id,
            usuarios.username,
            usuarios.rol,
            usuarios.last_session,
            personas.id
        FROM
            clientes
        JOIN 
            dispositivos ON dispositivos.id = clientes.id_dispositivo
        JOIN 
            personas ON personas.id = clientes.id_persona
        JOIN 
            colonias ON colonias.id = personas.id_colonia
        JOIN 
            usuarios ON usuarios.id_persona = clientes.id_persona
        WHERE
            clientes.id = '''+id_cliente
        cursor.execute(insert_query)
        
        # Obtener el resultado
        res = cursor.fetchone()

        dataRes = {

            "id_persona": res[17],
            
            "estado_servicio": res[1],
            "fecha_contratacion": res[2],

            "nombre": res[3],
            "app": res[4],
            "apm": res[5],
            "fech_nac": res[6],
            "sex": res[7],

            "colonia_nombre": res[9],
            "asentamiento": res[10],
            "ciudad": res[11],
            "codigo_postal": res[12],

            "id_user": res[13],
            "username": res[14],
            "rol": res[15],
            "last_session": res[16]
        }

        ######################################################################
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"msg": "Datos obtenidos correctamente", "data": dataRes}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

# QUERY's - REPORTES
@app.route('/crear-reporte/<id_cliente>', methods=['POST'])
@app.route('/obtener-all-reportes-by-client/<id_cliente>', methods=['GET'])
@app.route('/obtener-reporte/<id_cliente>/<id_reporte>', methods=['GET'])
#QUERY's - PERSONAS
@app.route('/actualizar-datos-personales/<id_persona>', methods=['PUT'])
#@jwt_required()
def actualizar_datos_personales(id_persona):
    '''
    # Obtener el rol desde los claims del JWT
    claims = get_jwt()  # Obtener la identidad (username) del token
    role = claims.get("role")

    # Verificar que el usuario tiene el rol de administrador o Capturista
    if role == 1 or role == 3: # 0 == Cliente, 2 == Técnico
        return jsonify({"mensaje":"No tienes autorizado el acceso."}), 403
    '''
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
        
        ######################################################################
        # Primero se debe registrar una persona
        persona = Persona();
        persona.id = id_persona;
        persona.nombre = request.form.get("nombre");
        persona.app = request.form.get("app");
        persona.apm = request.form.get("apm");

        # Extraer los atributos del objeto Persona como una tupla
        persona_data = (
            persona.nombre,
            persona.app,
            persona.apm,
            persona.id
        )

        insert_query1 = """
            UPDATE personas 
            SET nombre = %s, app = %s, apm = %s 
            WHERE id = %s;
            """
        cursor.execute(insert_query1, persona_data)

        # Verifica si se actualizó correctamente
        if cursor.rowcount == 0:
            return jsonify({"error": "Error al guardar los datos, ningún registro afectado"}), 500
        

        ######################################################################
        # Confirmar cambios
        connection.commit()
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"msg": "Datos actualizados correctamente"}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

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
@jwt_required()
def gets_all_clients():
    # Obtener el rol desde los claims del JWT
    claims = get_jwt()  # Obtener la identidad (username) del token
    role = claims.get("role")

    # Verificar que el usuario tiene el rol de administrador o Capturista
    if role == 0 or role == 2: # 0 == Cliente, 2 == Técnico
        return jsonify({"mensaje":"No tienes autorizado el acceso."}), 403
    
    connection = connect_to_database(); # Conectar a la base de datos
    print("Conexión a la base de datos ABIERTA.")
    cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
    
    try:
        insert_query = "SELECT * FROM clientes;"
        cursor.execute(insert_query)
        # Obtener el resultado
        res = cursor.fetchall()

        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"clientes": res}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

@app.route('/registrar-cliente', methods=['POST'])
@jwt_required()
def registrar_cliente():
    # Obtener el rol desde los claims del JWT
    claims = get_jwt()  # Obtener la identidad (username) del token
    role = claims.get("role")

    # Verificar que el usuario tiene el rol de administrador o Capturista
    if role == 0 or role == 2: # 0 == Cliente, 2 == Técnico
        return jsonify({"mensaje":"No tienes autorizado el acceso."}), 403

    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
        
        # Iniciar la transacción
        connection.start_transaction();

        # Primero se debe registrar una persona
        persona = Persona();
        persona.nombre = request.form.get("nombre");
        persona.app = request.form.get("app");
        persona.apm = request.form.get("apm");
        persona.fech_nac = request.form.get("fech_nac");
        persona.sex = request.form.get("sex");
        persona.id_colonia = request.form.get("id_colonia");
        
        # Extraer los atributos del objeto Persona como una tupla
        persona_data = (
            persona.nombre,
            persona.app,
            persona.apm,
            persona.fech_nac,
            persona.sex,
            persona.id_colonia
        )

        insert_query1 = """ INSERT INTO personas
        (nombre, app, apm, fech_nac, sex, id_colonia)
        VALUES (%s, %s, %s, %s, %s, %s) """
        cursor.execute(insert_query1, persona_data)
        persona.id = cursor.lastrowid;

        # Despues un cliente
        cliente = Cliente();
        cliente.id_persona = persona.id;
        cliente.fecha_contratacion = datetime.date(datetime.datetime.now().year,
                                                   datetime.datetime.now().month,
                                                   datetime.datetime.now().day);
        # Extraer los atributos del objeto Cliente como una tupla
        Cliente_data = (
            cliente.id_persona,
            cliente.fecha_contratacion,
            cliente.estado_servicio
        )
        insert_query2 = """ INSERT INTO clientes
        (id_persona, fecha_contratacion, estado_servicio)
        VALUES (%s, %s, %s) """
        cursor.execute(insert_query2, Cliente_data)

        # Al final se crea su usuario
        usuario = Usuario()
        usuario.id_persona = persona.id;
        usuario.username = generate_Pass(4)+"_"+persona.nombre
        usuario.password = generate_Pass(8);
        Usuario_data = (
            usuario.id_persona,
            usuario.username,
            usuario.password
        )
        insert_query3 = """ INSERT INTO usuarios
        (id_persona, username, password)
        VALUES (%s, %s, %s) """
        cursor.execute(insert_query3, Usuario_data)

        # Confirmar los cambios de la transacción
        connection.commit()
        datos = {
            "username": usuario.username,
            "password": usuario.password
        }
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"status": "Datos guardados correctamente", "datos": datos}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")


# ============== RESERVADO PARA CONSULTAS DEL OLAP ============== #



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

def generate_Pass(longitud=12):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(secrets.choice(caracteres) for i in range(longitud))
    return contrasena

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)