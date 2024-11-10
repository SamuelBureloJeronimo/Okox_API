from datetime import date


class Usuario:
    def __init__(self):
        self.id = None
        self.id_persona = None
        self.username = ""
        self.password = ""
        self.token = ""
        self.rol = 0 # 0 == Cliente, 1 == Capturista, 2 == Técnico, 3 == Administrador
        self.last_session = None