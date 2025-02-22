import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Cargar variables desde el archivo .env
load_dotenv()
if not os.path.exists(os.getenv("UPLOAD_FOLDER")):
    os.makedirs(os.getenv("UPLOAD_FOLDER"))


from config.jwt_conf import jwt
from config.bp_conf import bp
from config.mail_conf import mail

app = bp

# Habilitar CORS para todos los orígenes y rutas
CORS(app)