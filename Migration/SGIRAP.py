import mysql.connector

import Migration_Personas, Migration_Colonias, Migration_Municipios, Migration_Estados, Migration_Paises
import Migration_Administradores, Migration_Avisos, Migration_Clientes, Migration_Dispositivos
import Migration_Pagos, Migration_Mantenimientos, Migration_Presion
import Migration_Reportes, Migration_Suspensiones, Migration_Usuarios

# Conectarse a la base de datos MySQL
conn = mysql.connector.connect(
    host="localhost",        # O la IP de tu servidor MySQL
    user="root",       # El nombre de usuario de MySQL
    password="",# La contraseña de MySQL
    database="u839116441_sgirap"  # El nombre de la base de datos a la que te quieres conectar
)

cursor = conn.cursor()

cursor.execute(Migration_Paises.Migration_Paises.Table_Paises())
cursor.execute(Migration_Estados.Migration_Estados.Table_Estados())
cursor.execute(Migration_Municipios.Migration_Municipios.Table_Municipios())
cursor.execute(Migration_Colonias.Migration_Colonias.Table_Colonias())

cursor.execute(Migration_Personas.Migration_Personas.Table_Personas())
cursor.execute(Migration_Administradores.Migration_Administradores.Table_Administradores())

cursor.execute(Migration_Avisos.Migration_Avisos.Table_Avisos())


cursor.execute(Migration_Dispositivos.Migration_Dispositivos.Table_Dispositivos())
cursor.execute(Migration_Clientes.Migration_Clientes.Table_Clientes())
cursor.execute(Migration_Pagos.Migration_Pagos.Table_Pagos())
cursor.execute(Migration_Mantenimientos.Migration_Mantenimientos.Table_Mantenimientos())

cursor.execute(Migration_Presion.Migration_Presion.Table_Presion())
cursor.execute(Migration_Reportes.Migration_Reportes.Table_Reportes())
cursor.execute(Migration_Suspensiones.Migration_Suspensiones.Table_Suspensiones())
cursor.execute(Migration_Usuarios.Migration_Usuarios.Table_Usuarios())


# Guardar los cambios
conn.commit()