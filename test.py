from email.utils import parsedate_to_datetime
import secrets
import string
from flask import Flask, request, jsonify
import urllib.parse
from datetime import datetime, timedelta

from flask_jwt_extended import JWTManager, create_access_token, decode_token, get_jwt, jwt_required, get_jwt_identity # type: ignore
from flask_cors import CORS
from jwt import InvalidTokenError, ExpiredSignatureError, DecodeError

from models import Pais
from connection import connect_to_database
from mysql.connector import Error

from models.Usuario import Usuario
from models.Cliente import Cliente
from models.Persona import Persona

from collections import namedtuple

limite_diario = 1.0
REBT = 1.0

app = Flask(__name__)
# Habilitar CORS para todos los orígenes y rutas
CORS(app)

# Configura una clave secreta para firmar los tokens
LLAVE_JWT = "CLAVE-ULTRA-SECRETA"
app.config["JWT_SECRET_KEY"] = LLAVE_JWT
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=0.5)  # El token expira en 1 hora

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

        rol = res1[4]

        # Crea un token de acceso
        access_token = create_access_token(identity=username, additional_claims={"role": res1[4]})

        query = "SELECT id FROM clientes WHERE id_persona=%s;"
        cursor.execute(query, (res1[1],))
        cl_id = cursor.fetchone();


        query2 = "UPDATE usuarios SET token=%s, last_session=%s WHERE id=%s;"
        cursor.execute(query2, (access_token, datetime.now(), res1[0]))

        # Verifica si se actualizó correctamente
        if cursor.rowcount == 0:
            return jsonify({"error": "Error al guardar los datos, ningún registro afectado"}), 500
        
        # Cerrar la conexión
        connection.commit()
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"access_token": access_token, "rol": rol, "id_cliente": cl_id}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")
            
@app.route('/obtener-all-presion', methods=['GET'])
def get_presion_all():
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
        ######################################################################
        dataAVG = {
            "today": 0,
            "LastWeek": 0,
            "LastMonth": 0,
        }

        dataSUM = {
            "today": 0,
            "LastWeek": 0,
            "LastMonth": 0,
        }

        hora_actual = datetime.now()
        fecha = str(hora_actual.year)+"-"+str(hora_actual.month)+"-"+str(hora_actual.day)
        ayer = str(hora_actual.year)+"-"+str(hora_actual.month)+"-"+str(hora_actual.day-1)
        fecha1 = str(hora_actual.year)+"-"+str(hora_actual.month)+"-"+str(hora_actual.day-7)
        fecha2 = str(hora_actual.year)+"-"+str(hora_actual.month-1)+"-"+str(hora_actual.day)

        query_3 = "SELECT AVG(presion), SUM(presion) FROM presion WHERE fecha BETWEEN %s AND %s;"
        params = (fecha+" 00:00:00", fecha+" 23:59:59")
        cursor.execute(query_3, params)
        res = cursor.fetchone()
        # Verifica si hay datos reales en las columnas
        if res is None or all(value is None for value in res):  # Todas las columnas son NULL
            print("La consulta no devolvió datos.")
        else:
            dataAVG["today"] = res[0]
            dataSUM["today"] = res[1]/60
        
        query_3 = "SELECT AVG(presion), SUM(presion) FROM presion WHERE fecha BETWEEN %s AND %s;"
        params = (fecha1+" 00:00:00", ayer+" 23:59:59")
        cursor.execute(query_3, params)
        res1 = cursor.fetchone()
        # Verifica si hay datos reales en las columnas
        if res1 is None or all(value is None for value in res1):  # Todas las columnas son NULL
            print("La consulta no devolvió datos.")
        else:
            dataAVG["LastWeek"] = res1[0]
            dataSUM["LastWeek"] = res1[1]/60

        query_3 = "SELECT AVG(presion), SUM(presion) FROM presion WHERE fecha BETWEEN %s AND %s;"
        params = (fecha2+" 00:00:00", ayer+" 23:59:59")
        cursor.execute(query_3, params)
        res2 = cursor.fetchone()
        # Verifica si hay datos reales en las columnas
        if res2 is None or all(value is None for value in res2):  # Todas las columnas son NULL
            print("La consulta no devolvió datos.")
        else:
            dataAVG["LastMonth"] = res2[0]
            dataSUM["LastMonth"] = res2[1]/60
        
        ######################################################################
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"msg": "Datos obtenidos correctamente", "dataAVG": dataAVG, "dataSUM": dataSUM}), 200
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
def get_data_client(id_cliente):
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
            colonias.nombre AS colonia_nombre,
            colonias.asentamiento,
            municipios.nombre,
            colonias.codigo_postal,
            usuarios.username,
            usuarios.rol,
            usuarios.last_session,
            personas.id
        FROM
            clientes
        JOIN 
            personas ON personas.id = clientes.id_persona
        JOIN 
            colonias ON colonias.id = personas.id_colonia
        JOIN 
            municipios ON municipios.id = colonias.municipio
        JOIN 
            usuarios ON usuarios.id_persona = clientes.id_persona
        WHERE
            clientes.id = '''+id_cliente
        cursor.execute(insert_query)
        
        # Obtener el resultado
        res = cursor.fetchone()

        dataRes = {
            
            "estado_servicio": res[1],
            "fecha_contratacion": res[2],

            "nombre": res[3],
            "app": res[4],
            "apm": res[5],
            "fech_nac": res[6],
            "sex": res[7],

            "colonia_nombre": res[8],
            "asentamiento": res[9],
            "ciudad": res[10],
            "codigo_postal": res[11],

            "username": res[12],
            "rol": res[13],
            "last_session": res[14],

            "id_persona": res[15]
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
def create_reporte(id_cliente):
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas

        ##########################################################################

        # Verificar si ya existe un registro para la fecha actual
        # Obtener la fecha actual
        fecha = datetime.now().strftime('%Y-%m-%d')

        query_verificar = "SELECT * FROM reportes WHERE id_cliente = %s AND fecha_subida BETWEEN %s AND %s;"
        params = (id_cliente, f"{fecha} 00:00:00", f"{fecha} 23:59:59")
        cursor.execute(query_verificar, params)
        
        registro_existente = cursor.fetchall()

        if registro_existente:
            return jsonify({'error': 'Ya existe un registro para el día de hoy.'}), 400
        

        insert_query = "INSERT INTO reportes (id_cliente, mensaje) VALUES (%s,%s);"
        data = (id_cliente, request.form.get("mensaje"))
        cursor.execute(insert_query, data)

        ##########################################################################

        # Cerrar la conexión
        cursor.close()
        connection.commit()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"msg": "Reporte registrado"}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

@app.route('/obtener-all-reportes-by-client/<id_cliente>', methods=['GET'])
@app.route('/obtener-reporte/<id_cliente>/<id_reporte>', methods=['GET'])
@app.route('/obtener-notificaciones/<id_cliente>', methods=['GET'])
def get_noti(id_cliente):
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas

        ##########################################################################

        insert_query = '''
                        SELECT mensaje FROM
                            notificaciones
                        WHERE
                            cliente_id=%s;
                        '''
        cursor.execute(insert_query, (id_cliente,))
        # Obtener el resultado
        res = cursor.fetchall()
        
        ##########################################################################

        # Cerrar la conexión
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"lista": res}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")
#QUERY's - PERSONAS
@app.route('/actualizar-datos-personales/<id_persona>', methods=['PUT'])
def actualizar_datos_personales(id_persona):
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

@app.route('/obtener-presion/<id_cliente>', methods=['GET'])
def get_presion(id_cliente):
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
        ######################################################################

        dataAVG = {
            "today": 0,
            "LastWeek": 0,
            "LastMonth": 0,
        }

        dataSUM = {
            "today": 0,
            "LastWeek": 0,
            "LastMonth": 0,
        }
        hora_actual = datetime.now()
        fecha = str(hora_actual.year)+"-"+str(hora_actual.month)+"-"+str(hora_actual.day)
        ayer = str(hora_actual.year)+"-"+str(hora_actual.month)+"-"+str(hora_actual.day-1)
        fecha1 = str(hora_actual.year)+"-"+str(hora_actual.month)+"-"+str(hora_actual.day-7)
        fecha2 = str(hora_actual.year)+"-"+str(hora_actual.month-1)+"-"+str(hora_actual.day)

        query_3 = "SELECT AVG(presion.presion), clientes.Litros_totales_dia FROM presion JOIN clientes ON clientes.id=presion.id_cliente WHERE id_cliente=%s AND fecha BETWEEN %s AND %s;"
        params = (id_cliente, fecha+" 00:00:00", fecha+" 23:59:59")
        cursor.execute(query_3, params)
        res = cursor.fetchone()

        # Verifica si hay datos reales en las columnas
        if res is None or all(value is None for value in res):  # Todas las columnas son NULL
            print("La consulta no devolvió datos.")
        else:
            dataAVG["today"] = res[0]
            dataSUM["today"] = res[1]
        
        params = (id_cliente, fecha1+" 00:00:00", ayer+" 23:59:59")
        cursor.execute(query_3, params)
        res1 = cursor.fetchone()
                # Verifica si hay datos reales en las columnas
        if res1 is None or all(value is None for value in res1):  # Todas las columnas son NULL
            print("La consulta no devolvió datos.")
        else:
            dataAVG["LastWeek"] = res1[0]
            dataSUM["LastWeek"] = res1[1]

        params = (id_cliente, fecha2+" 00:00:00", ayer+" 23:59:59")
        cursor.execute(query_3, params)
        res2 = cursor.fetchone()
        if res2 is None or all(value is None for value in res2):  # Todas las columnas son NULL
            print("La consulta no devolvió datos.")
        else:
            dataAVG["LastMonth"] = res2[0]
            dataSUM["LastMonth"] = res2[1]
        
        ######################################################################
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"msg": "Datos obtenidos correctamente", "dataAVG": dataAVG, "dataSUM": dataSUM}), 200
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
def get_all_reports():
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas

        ##########################################################################

        insert_query = "SELECT * FROM reportes;"
        cursor.execute(insert_query)

        data = convertToObject(cursor);
        
        ##########################################################################

        # Cerrar la conexión
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify(data), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

@app.route('/obtener-reporte/<id_reporte>', methods=['GET'])
@app.route('/update-reporte/<id_reporte>', methods=['PUT'])
# Query's - SUSPENSIÓN
@app.route('/registrar-suspension', methods=['POST'])
def create_suspension():
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
        ######################################################################

        # Extrae los datos del ESP32 enviados en formato JSON
        data = request.json
        motivo = data.get('motivo')
        duracion_dias = data.get('duracion')
        id_cliente = data.get('id_cliente')

        sql = "SELECT * FROM suspensiones WHERE id_cliente=%s;"
        params = (id_cliente,)
        cursor.execute(sql, params);

        res = cursor.fetchall();
        if res:
            fecha = str(res[0][4].date())
            # Convertir la cadena a datetime
            fecha_obj = datetime.strptime(fecha, "%a, %d %b %Y %H:%M:%S GMT")
            # Incrementar un día
            fecha_incrementada = fecha_obj + timedelta(days=1)
            #if(fecha_incrementada > datetime.now().date()):
            return jsonify({"info": "El servicio esta suspendido", "fechas": fecha_incrementada, "now":str(datetime.now().date())}), 200


        sql = "INSERT INTO suspensiones (motivo, duracion_dias, id_cliente) VALUES (%s, %s,%s);"
        cursor.execute(sql, (motivo, duracion_dias, id_cliente));

        sql = "UPDATE clientes SET estado_servicio=1 WHERE id=%s;"
        cursor.execute(sql, (id_cliente,));

        ######################################################################
        # Confirmar cambios
        connection.commit()
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"msg": "Se suspendio el servicio con éxito"}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

@app.route('/restablecer-servicios/<id_cliente>', methods=['PUT'])
def rest(id_cliente):
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
        ######################################################################
        query = "SELECT * FROM clientes WHERE id=%s;"
        cursor.execute(query, (id_cliente,));

        res = cursor.fetchone()

        if(res is None):
                return jsonify({"Error": "Cliente no encontrado ID="+id_cliente}), 200
        

        insert_query1 = """
            UPDATE clientes 
            SET estado_servicio = 0,
            umbral_max = %s 
            WHERE id = %s;
            """
        cursor.execute(insert_query1, (res[5]+res[6],id_cliente));

        insert_query1 = """
            INSERT INTO notificaciones (cliente_id, mensaje) VALUES (%s, %s);
            """
        cursor.execute(insert_query1, (id_cliente,"Servicios restablecidos"));
    
        ######################################################################
        # Confirmar cambios
        connection.commit()
        global limite_diario  # Indicamos que queremos usar la variable global
        limite_diario = limite_diario+REBT;
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"msg": "Se restablecieron los servicios con éxito"}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

# ============== RESERVADO PARA CAPTURISTAS Y ADMINISTRADORES ============== #
# Query's - CLIENTES
@app.route('/obtener-all-clientes', methods=['GET'])
def gets_all_clients():
    
    connection = connect_to_database(); # Conectar a la base de datos
    print("Conexión a la base de datos ABIERTA.")
    cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
    
    try:
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
            colonias.nombre AS colonia_nombre,
            colonias.asentamiento,
            municipios.nombre,
            colonias.codigo_postal,
            usuarios.username,
            usuarios.rol,
            usuarios.last_session,
            personas.id
        FROM
            clientes
        JOIN 
            personas ON personas.id = clientes.id_persona
        JOIN 
            colonias ON colonias.id = personas.id_colonia
        JOIN 
            municipios ON municipios.id = colonias.municipio
        JOIN 
            usuarios ON usuarios.id_persona = clientes.id_persona
        '''
        cursor.execute(insert_query)
        # Obtener el resultado
        res = cursor.fetchall()

        allClients = []

        for row in res:           
            dataRes = {
                "id": row[0],
                "estado_servicio": row[1],
                "fecha_contratacion": row[2],

                "nombre": row[3],
                "app": row[4],
                "apm": row[5],
                "fech_nac": row[6],
                "sex": row[7],

                "colonia_nombre": row[8],
                "asentamiento": row[9],
                "ciudad": row[10],
                "codigo_postal": row[11],

                "username": row[12],
                "rol": row[13],
                "last_session": row[14],

                "id_persona": row[15]
            }
            allClients.append(dataRes)

        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify(allClients), 200
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
def registrar_cliente():
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
        # Extraer los atributos del objeto Cliente como una tupla
        Cliente_data = (
            cliente.id_persona,
            cliente.estado_servicio
        )
        insert_query2 = """ INSERT INTO clientes
        (id_persona, estado_servicio)
        VALUES (%s, %s) """
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



@app.route('/get-paises', methods=['GET'])
def get_paises():
    
    connection = connect_to_database(); # Conectar a la base de datos
    print("Conexión a la base de datos ABIERTA.")
    cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
    
    try:
        # Obtener los nombres de las columnas

        insert_query = "SELECT id, nombre FROM paises;"
        cursor.execute(insert_query)

        data = convertToObject(cursor);
        
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify(data), 200
    
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

@app.route('/get-estados/<id_pais>', methods=['GET'])
def get_estados(id_pais):
    
    connection = connect_to_database(); # Conectar a la base de datos
    print("Conexión a la base de datos ABIERTA.")
    cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
    
    try:

        insert_query = "SELECT id, nombre FROM estados WHERE pais=%s;"
        cursor.execute(insert_query, (id_pais,))

        data = convertToObject(cursor);

        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify(data), 200
    
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

@app.route('/get-municipios/<id_estado>', methods=['GET'])
def get_municipios(id_estado):
    
    connection = connect_to_database(); # Conectar a la base de datos
    print("Conexión a la base de datos ABIERTA.")
    cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
    
    try:

        insert_query = "SELECT id, nombre FROM municipios WHERE estado=%s;"
        cursor.execute(insert_query, (id_estado,))

        data = convertToObject(cursor);

        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify(data), 200
    
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

@app.route('/get-colonias/<id_municipio>', methods=['GET'])
def get_colonias(id_municipio):
    
    connection = connect_to_database(); # Conectar a la base de datos
    print("Conexión a la base de datos ABIERTA.")
    cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
    
    try:

        insert_query = "SELECT id, nombre FROM colonias WHERE municipio=%s;"
        cursor.execute(insert_query, (id_municipio,))
        data = convertToObject(cursor);

        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify(data), 200
    
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
@app.route('/registrar-dispositivo', methods=['POST'])
def registrar_dispositivo():
    try:
        connection = connect_to_database(); # Conectar a la base de datos
        print("Conexión a la base de datos ABIERTA.")
        cursor = connection.cursor(); # Crear un cursor para ejecutar las consultas
        ######################################################################

        # Extrae los datos del ESP32 enviados en formato JSON
        data = request.json
        id_cliente = data.get('id_cliente')
        Wifi_MacAddress = data.get('Wifi_MacAddress')
        sql = "INSERT INTO dispositivos (id_cliente, Wifi_MacAddress) VALUES (%s,%s);"
        cursor.execute(sql, (id_cliente, Wifi_MacAddress));

        ######################################################################
        # Confirmar cambios
        connection.commit()
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")
        return jsonify({"msg": "El dispositivo fue creado con éxito"}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": e.msg}), 500
    finally:
        # Cerrar el cursor y la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos cerrada.")

# ============== IoT y Servidor ============== #
# Se obtienen los datos iniciales: id_cliente y volumen_Litros
@app.route('/initialitation/<codedMac>', methods=['GET'])
def initialitation(codedMac):
    
    hora_actual = datetime.now()
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
        cursor = connection.cursor()

        query_2 = '''
                SELECT clientes.id,
                clientes.Litros_totales_dia,
                clientes.estado_servicio
                FROM clientes 
                JOIN dispositivos ON dispositivos.id_cliente = clientes.id
                WHERE dispositivos.Wifi_MacAddress = %s;
                '''
        cursor.execute(query_2, (decodedMAC,))
        # Obtener el resultado
        res1 = cursor.fetchone()
        # Verificar si se obtuvo un resultado
        if res1 is None:
            return jsonify({"error": "El dispositivo no esta registrado."}), 500
            
        id_cliente = res1[0]
        Litros_totales_dia = res1[1]
        estado_servicio = res1[2]
        
        query_3 = "SELECT AVG(presion.presion), clientes.Litros_totales_dia FROM presion JOIN clientes ON clientes.id=presion.id_cliente WHERE id_cliente=%s AND fecha BETWEEN %s AND %s;"
        params = (id_cliente, fecha+" 00:00:00", fecha+" 23:59:59")
        cursor.execute(query_3, params)

        # Obtener el resultado
        res1 = cursor.fetchone()

        
        if(estado_servicio == 1):
            return jsonify({"st": 901, "id_cliente": id_cliente, "volumen_Litros": Litros_totales_dia}), 200;   

        return jsonify({"res": "Datos obtenidos correctamente", "id_cliente": id_cliente, "volumen_Litros": Litros_totales_dia}), 200
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
        return jsonify({"error": "Datos no válidos"}), 

    # Conectar a la base de datos
    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    # Insertar datos en la base de datos
    try:   
        cursor = connection.cursor()
        query = "SELECT * FROM clientes WHERE id=%s;"
        cursor.execute(query, (id_cliente,));

        res = cursor.fetchone()

        if(res is None):
                return jsonify({"Error": "Cliente no encontrado ID="+id_cliente}), 200
        
        if float(res[2]) == 1:
            return jsonify({"st": 901}), 200
        
        if float(volumen_Litros) >= float(res[5]):
   
            insert_query = "INSERT INTO suspensiones (motivo,id_cliente) VALUES ('Limite diario excedido',%s);"
            cursor.execute(insert_query, (id_cliente,))

            insert_query = "INSERT INTO notificaciones (cliente_id, mensaje) VALUES (%s, 'Limite diario excedido');"
            cursor.execute(insert_query, (id_cliente,))
            
            insert_query = "INSERT INTO presion (presion, id_cliente) VALUES (%s, %s);"
            cursor.execute(insert_query, (presion, id_cliente))

            insert_query = "UPDATE clientes SET Litros_totales_dia=%s, estado_servicio=1 WHERE id=%s;"
            cursor.execute(insert_query, (volumen_Litros, id_cliente))

            connection.commit()
            cursor.close()
            return jsonify({"res": "Tu servicio a sido suspendido por superar los "+str(res[5])+"L por dia."}), 200

        if(float(presion) > 1.0):
            cursor = connection.cursor()
            insert_query = "INSERT INTO presion (presion, id_cliente) VALUES (%s, %s);"
            cursor.execute(insert_query, (presion, id_cliente))

            insert_query = "UPDATE clientes SET Litros_totales_dia=%s WHERE id=%s;"
            cursor.execute(insert_query, (volumen_Litros, id_cliente))

            connection.commit()
            cursor.close()
            
            return jsonify({"status": "Datos guardados correctamente", "cod": 101}), 200
        else:
            insert_query = "INSERT INTO suspensiones (motivo,id_cliente) VALUES ('Limite diario excedido',%s);"
            cursor.execute(insert_query, (id_cliente,))

            insert_query = "INSERT INTO notificaciones (cliente_id, mensaje) VALUES (%s, 'Servicio suspendido por baja presión');"
            cursor.execute(insert_query, (id_cliente,))
            
            insert_query = "INSERT INTO presion (presion, id_cliente) VALUES (%s, %s);"
            cursor.execute(insert_query, (presion, id_cliente))

            insert_query = "UPDATE clientes SET Litros_totales_dia=%s, estado_servicio=1 WHERE id=%s;"
            cursor.execute(insert_query, (volumen_Litros, id_cliente))

            connection.commit()
            cursor.close()
            return jsonify({"res": "Tu servicio a sido suspendido por baja presión. Es posible que haya fugas."}), 200
    except Error as e:
        print("Error al insertar datos", e)
        return jsonify({"error": "Error al insertar o actualizar datos"}), 500
    finally:
        connection.close()

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

def generate_Pass(longitud=12):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(secrets.choice(caracteres) for i in range(longitud))
    return contrasena

def convertToObject(cursor):
    columnas = [column[0] for column in cursor.description]  # Obtiene los nombres de las columnas
    # Usar namedtuple para tratar las filas como objetos
    TABLE = namedtuple('TABLE', columnas)  # Crear una clase con los nombres de las columnas como atributos
    response = cursor.fetchall()

    # Crear una lista de objetos Pais
    object_data = [TABLE(*row) for row in response]
    # Retornar la respuesta como JSON con los nombres de las columnas y los datos
    return [object._asdict() for object in object_data]  # Convertir namedtuple a diccionario para JSON


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)