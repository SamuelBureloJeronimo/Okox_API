from flask_jwt_extended import JWTManager
from config.app import app

# Configuración de la clave secreta para JWT
app.config["JWT_SECRET_KEY"] = "LLAVE-ULTRA-SECRETA"  # Cambia esto en producción
jwt = JWTManager(app)
