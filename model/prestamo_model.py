class Prestamo:
    id: str
    usuario_id: str
    monto: float
    tasa_interes: float
    plazo_meses: int
    estado: str
    fecha_solicitud: str

    def __init__(self, id: str, usuario_id: str, monto: float, tasa_interes: float, plazo_meses: int, estado: str, fecha_solicitud: str):
        self.id = id
        self.usuario_id = usuario_id
        self.monto = monto
        self.tasa_interes = tasa_interes
        self.plazo_meses = plazo_meses
        self.estado = estado
        self.fecha_solicitud = fecha_solicitud