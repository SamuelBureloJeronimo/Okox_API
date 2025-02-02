from flask import Blueprint
from database.db import *


BD_Capturista = Blueprint('BD_Capturista', __name__)

@BD_Capturista.route('/create-cliente', methods=['POST'])
def create_user():

    pass