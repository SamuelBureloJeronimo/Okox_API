class Cliente:
    def __init__(self):
        self.id = None
        self.id_persona = None  # Tipo Int o None
        self.estado_servicio = 0  # 0 == Activo, 1 == Suspendido
        self.fecha_contratacion = None  # Tipo DateTime