from config.app import app
from database.db import *
from models.all_models import *


if __name__ == '__main__':
    
    try:
        Base.metadata.create_all(engine)
        print("Tablas creadas correctamente")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
    
    try:
        # Intentar hacer una consulta simple para verificar la conexión
        connection = engine.connect()
        connection.close()
        print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print(f"Error de conexión: {e}")

    app.run(host='0.0.0.0', port=5000, debug=True)