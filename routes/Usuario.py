import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from database.db import *
from werkzeug.utils import secure_filename

from models.Usuarios import Usuarios
from models.Personas import Personas

#<NombreDelObjeto> = Blueprint('NombreDelObjeto', __name__, url_prefix='/prefijo')
BP_User = Blueprint('BP_User', __name__, url_prefix='/usuario')

#@<NombreDelObjeto>.route('/Nombre-de-laruta', methods=['GET', 'POST', 'PUT', 'DELETE'])
@BP_User.route('/get-my-data', methods=['GET'])
#def <nombreDelMetodo>():
@jwt_required()
def get_my_data():

    jwt_data = get_jwt()  # Obtiene todo el payload del JWT
    rfc = jwt_data.get("rfc")  # Si guardaste "nombre" en el token

    #<variable> = Session()
    session = Session()
    #<variable> = session.query(<ClaseDeLaTabla>).get(<Hace referencia al llave primaria>)
    user = session.query(Usuarios).get(rfc)
    persona = session.query(Personas).get(rfc)


    if user is None:
        return jsonify("Usuario no encontrado"), 400
    
    user_comp = {**user.to_dict(), **persona.to_dict()};

    session.close()
    return jsonify(user_comp), 200