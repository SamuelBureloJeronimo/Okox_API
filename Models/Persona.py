class Persona:
    def __init__(self):
        self.id = None
        self.nombre = ""
        self.app = ""
        self.apm = ""
        self.fech_nac = None
        self.rol = 0 # 0 == Cliente, 1 == Capturista, 2 == Técnico, 3 == Administrador
        self.sex = ""
        self.id_colonia = None