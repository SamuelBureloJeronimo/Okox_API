from flask import Blueprint, jsonify
from database.db import *
from sqlalchemy import exc

from models.address.Colonias import Colonias
from models.address.Estados import Estados
from models.address.Municipios import Municipios
from models.address.Paises import Paises

BP_Address = Blueprint('BP_Address', __name__)


@BP_Address.route('/get-paises', methods=['GET'])
def get_paises():

    try:        
        with Session() as session:
            paises = session.query(Paises).all();
            if(paises is None):
                return jsonify({
                    "mensaje": "No se encontro paises"
                }), 400
        
            # Convertir lista de objetos en lista de diccionarios
            paises_list = [pais.to_dict() for pais in paises]
            
            return jsonify(paises_list), 200

    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 

    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": "Error en la base de datos"
        }), 500

@BP_Address.route('/get-estados/<id_pais>', methods=['GET'])
def get_estados(id_pais):
    try:
        with Session() as session:

            estados = session.query(Estados).filter_by(pais=id_pais).all();
            
            if(estados is None):
                return jsonify({
                "mensaje": "No se encontro paises"
                }), 400
        
            # Convertir lista de objetos en lista de diccionarios
            estados_list = [est.to_dict() for est in estados]

            return jsonify(estados_list), 200
        
    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 

    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": "Error en la base de datos"
        }), 500

@BP_Address.route('/get-municipios/<id_estado>', methods=['GET'])
def get_municipios(id_estado):
    try:
        with Session() as session:

            mun = session.query(Municipios).filter_by(estado=id_estado).all();
            
            if(mun is None):
                return jsonify({
                "mensaje": "No se encontro Municipios"
                }), 400

            # Convertir lista de objetos en lista de diccionarios
            municipios_list = [m.to_dict() for m in mun]

            return jsonify(municipios_list), 200
        
    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 

    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": "Error en la base de datos"
        }), 500


@BP_Address.route('/get-colonias/<id_municipio>', methods=['GET'])
def get_colonias(id_municipio):

    try:
        with Session() as session:
            if not session.is_active:
                session = Session()  # Reabrir la sesión

            colns = session.query(Colonias).filter_by(municipio=id_municipio).all();
        
            if(colns is None):
                return jsonify({
                "mensaje": "No se encontro Colonias"
                }), 400

            # Convertir lista de objetos en lista de diccionarios
            colonias_list = [col.to_dict() for col in colns]

            return jsonify(colonias_list), 200
        
    except exc.IntegrityError as e:
        session.rollback()
        return jsonify({
            "error": (e.args)
        }), 400 

    except exc.SQLAlchemyError as e:
        session.rollback()
        return jsonify({
            "error": "Error en la base de datos"
        }), 500
