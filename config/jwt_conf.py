from datetime import timedelta
from flask_jwt_extended import JWTManager
from config.app import app

# Configuración de la clave secreta para JWT
app.config["JWT_SECRET_KEY"] = "LLAVE-ULTRA-SECRETA"  # Cambia esto en producción
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=0.5)  # Expira en 1 hora
jwt = JWTManager(app)
