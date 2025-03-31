import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from config.middlewares import with_session
from database.db import *
from models.MyCompany import MyCompany
from werkzeug.utils import secure_filename

from models.Posts import Posts

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


@BP_SuperUser.route('/subir-post', methods=['POST'])
@jwt_required()
@with_session
def upload_video(session):
    required_fields = ["title", "description"]
    missing_fields = [field for field in required_fields if not request.form.get(field)]

    # Validar si falta algún campo
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400
    
    if ('video' not in request.files) and ('foto' not in request.files):
        return jsonify({'error': 'Debes enviar un archivo Video/Imagen'}), 400
    
    post = Posts()

    post.tittle = request.form.get("title")
    post.description = request.form.get("description")

    video = request.files.get('video')
    foto = request.files.get('foto')

    if video:
        video = request.files['video']
        filename = secure_filename(video.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_nombre = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        video_path = os.path.join(os.getenv("UPLOAD_FOLDER")+"publicaciones/videos/", nuevo_nombre)
        post.path_file = "/publicaciones/videos/"+nuevo_nombre;
        post.type = 1;
        video.save(video_path)
    elif foto:
        foto = request.files['foto']
        filename = secure_filename(foto.filename)
        ext = os.path.splitext(filename)[1]  # Obtener la extensión

        nuevo_foto = f"{uuid.uuid4()}{ext}"  # Generar un nuevo nombre único
        foto_path = os.path.join(os.getenv("UPLOAD_FOLDER")+"publicaciones/fotos/", nuevo_foto)
        post.path_file = "/publicaciones/fotos/"+nuevo_foto;
        post.type = 0;
        foto.save(foto_path)

    session.add(post)
    session.commit()

    return jsonify({'message': 'Video subido con éxito'})