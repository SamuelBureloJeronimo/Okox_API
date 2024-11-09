class Administrador:
    def __init__(self):
        self.id = None
        self.fech_alta = None  # Tipo Date
        self.estado = 0 # 0 == Desconectado || 1 == Activo || 2 == Banneado
        self.id_persona = None  # Tipo Int o None