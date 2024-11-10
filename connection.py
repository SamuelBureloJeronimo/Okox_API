import mysql.connector
from mysql.connector import Error
# Configuración de la conexión a la base de datos MySQL
def connect_to_database():
    try:
        '''
        connection = mysql.connector.connect(
            host="srv1601.hstgr.io",  # Cambia esto por la dirección de tu servidor MySQL
            user="u839116441_admin",
            password="VepZHycV~p3:",
            database="u839116441_sgirap"
        )
        '''
        connection = mysql.connector.connect(
            host="localhost",  # Cambia esto por la dirección de tu servidor MySQL
            user="root",
            password="",
            database="u839116441_sgirap"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error al conectar a la base de datos", e)
        return None