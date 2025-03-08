import uuid
import hashlib

class Prestamo:
    id: str
    usuario_id: str
    monto: float
    tasa_interes: float
    plazo_meses: int
    estado: str
    fecha_solicitud: str

    def __init__(self, usuario_id: str, monto: float, tasa_interes: float, plazo_meses: int, estado: str, fecha_solicitud: str):
        self.id = generate_transaction_id(usuario_id, monto, fecha_solicitud)
        self.usuario_id = usuario_id
        self.monto = monto
        self.tasa_interes = tasa_interes
        self.plazo_meses = plazo_meses
        self.estado = estado
        self.fecha_solicitud = fecha_solicitud

def generate_transaction_id(user_id, amount, timestamp):
    data = f"{user_id}{amount}{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]