class User:
    dni: str
    nombre: str
    apellidos: str
    email: str
    telefono: str

    def __init__(self,dni: str,nombre: str,apellidos: str,email: str,telefono: str):
        self.dni = dni
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono