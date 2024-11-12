# Conectarse a la base de datos MySQL
import mysql.connector


conn = mysql.connector.connect(
    host="localhost",        # O la IP de tu servidor MySQL
    user="root",       # El nombre de usuario de MySQL
    password="",# La contraseña de MySQL
    database="u839116441_sgirap"  # El nombre de la base de datos a la que te quieres conectar
)

cursor = conn.cursor()

cursor.execute(
    """
    CREATE VIEW vista_consumo_cliente AS
    SELECT
        id_cliente,
        id_colonia,
        SUM(presion),
        AVG(presion),
        MAX(presion) FROM presion
    FROM 
        presion
    GROUP BY 
        id_cliente, id_presion;
    """
)