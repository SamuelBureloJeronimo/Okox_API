import secrets
import string
import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from database.db import *
from index import with_session
from models.Mantenimientos import Mantenimientos
from models.MyCompany import MyCompany
from models.Personas import Personas
from models.Usuarios import Usuarios
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename

# Cargar variables desde el archivo .env
load_dotenv()

BP_SuperUser = Blueprint('BP_SuperUser', __name__, url_prefix='/super')

@BP_SuperUser.route('/change-image', methods=['POST'])
@jwt_required()
@with_session
def change_image(session):
    
    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    rfc = jwt_data.get("rfc")  # "sub" es el campo "identity" por defecto

    # Validar si la imagen está presente
    if 'img' not in request.files:
        return jsonify({"error": "El campo 'img' es obligatorio"}), 400
    
    rfc = "BUJS030806UM7";
    # Procesar la imagen
    file = request.files['img']
    okox = session.query(MyCompany).filter_by(rfc=rfc).first()
    if okox.logo == "/company/default_perfil.png":
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_nombre = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        filepath = os.path.join(os.getenv("UPLOAD_FOLDER")+"image/company/", nuevo_nombre)
        file.save(filepath)
        session.query(MyCompany).filter(MyCompany.rfc == rfc).update({MyCompany.logo: "/company/"+nuevo_nombre})
        session.commit()
    else:
        file.save("public/image/"+okox.logo)
    
    return jsonify("¡Imagen actualizada con éxito!"), 200