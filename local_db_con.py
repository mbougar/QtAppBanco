import sqlite3
from model.user_model import User
from model.prestamo_model import Prestamo
from datetime import datetime,timedelta

## En lugar de hacerlo todo aqui, si queremos mejorarlo, podemos dejar la conexion con la base de datos aqui y hacer una clase para cada tabla de la base de datos
## y hacer las operaciones de la base de datos en esas clases, simplemente pasando una conexion a la funcion, para que sea mas facil de mantener y de entender

class LocalDbConn:
    _instance = None

    actualUser: User = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LocalDbConn, cls).__new__(cls)
        return cls._instance
    
    
    def __init__(self):
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        
        try:
            # Crear las tablas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    dni VARCHAR(255) PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    apellidos VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    telefono VARCHAR(255) NOT NULL,
                    fecha_registro DATETIME NOT NULL
                );""")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    iban VARCHAR(255) PRIMARY KEY,
                    usuario_id VARCHAR(255) NOT NULL,
                    tipo VARCHAR(255) NOT NULL,
                    saldo REAL NOT NULL,
                    moneda VARCHAR(255) NOT NULL,
                    fecha_creacion DATETIME NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES users(dni) ON DELETE CASCADE
                );""")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cuenta_id VARCHAR(255) NOT NULL,
                monto REAL NOT NULL,
                tipo VARCHAR(255) NOT NULL,
                descripcion VARCHAR(255) NOT NULL,
                fecha DATETIME NOT NULL,
                FOREIGN KEY (cuenta_id) REFERENCES accounts(iban) ON DELETE CASCADE
            );""")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id VARCHAR(255) PRIMARY KEY,
                usuario_id VARCHAR(255) NOT NULL,
                monto FLOAT NOT NULL,
                tasa_interes FLOAT NOT NULL,
                plazo_meses INTEGER NOT NULL,
                estado VARCHAR(255) NOT NULL,
                fecha_solicitud DATETIME NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES users(dni) ON DELETE CASCADE
            );""")
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                numero VARCHAR(255) PRIMARY KEY,
                account_id VARCHAR(255) NOT NULL,
                tipo VARCHAR(255) NOT NULL,
                fecha_vencimiento DATETIME NOT NULL,
                cvv VARCHAR(255) NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts(iban) ON DELETE CASCADE
            );""")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id VARCHAR(255) NOT NULL,
                monto REAL NOT NULL,
                descripcion VARCHAR(255) NOT NULL,
                fecha_renovacion INT NOT NULL,
                renovar BOOLEAN NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts(iban) ON DELETE CASCADE
            );""")
            conn.commit()
        except:
            print("Algo salió mal al iniciar la base de datos")
            conn.rollback()
        cursor.close()

    #funcion para obtener una conexion a la base de datos
    def conn():
        with sqlite3.connect("local_db.db") as conn:
            return conn
    
    ## USER

    def insertUser(userToInsert:User):
        
        if (userToInsert.dni == "" or userToInsert.nombre == "" or userToInsert.apellidos == "" or userToInsert.email == "" or userToInsert.telefono == ""):
                raise Exception("Faltan datos")
        ## Controlar la excepcion en la ui para mostrar un mensaje personalizado

        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            
            cursor.execute("""
            INSERT INTO users (dni, nombre, apellidos, email, telefono,fecha_registro) 
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                userToInsert.dni, 
                userToInsert.nombre, 
                userToInsert.apellidos, 
                userToInsert.email, 
                userToInsert.telefono,
                datetime.now()))
            conn.commit()
        except Exception as e:
            print(f"Algo salió mal al insertar el usuario: {e}")
            conn.rollback
        
        conn.close()
        
    def comprobarDni(dni): # puede devolver un booleano o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE dni = ?", (dni,))
            user = cursor.fetchone()
            conn.commit()
            conn.close()
            return user != None
        except:
            print("Algo salió mal al buscar el dni")
            conn.rollback()
            conn.close()
    
    def comprobarEmail(email): # puede devolver un booleano o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.commit()
            conn.close()
            return user != None
        except:
            print("Algo salió mal al buscar el email")
            conn.rollback()
            conn.close()

    def cargarUserInfo(mail): # puede devolver un usuario o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (mail,))
            user = cursor.fetchone()
            conn.commit()
            conn.close()
            LocalDbConn.actualUser = User(user[0], user[1], user[2], user[3], user[4])
        except:
            print("Algo salió mal al buscar el usuario")
            conn.rollback()
            conn.close()
        
    def deleteUser():
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE dni = ?", (LocalDbConn.actualUser.dni,))
            conn.commit()
        except:
            print("Algo salió mal al borrar el usuario")
            conn.rollback()
        conn.close()

    ## CUENTAS

    def obtenerUltimasTresCuentasDeUsuario(): # puede devolver una lista de cuentas o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM accounts WHERE usuario_id = ? ORDER BY fecha_creacion DESC LIMIT 3", (LocalDbConn.actualUser.dni,))
            accounts = cursor.fetchall()
            conn.commit()
            conn.close()
            return accounts
        except Exception as e:
            print(f"Algo salió mal al buscar las cuentas: {e}")
            conn.rollback()
            conn.close()

    ## TARJETAS

    def obtenerTarjetaDeCuenta(cuenta_id): # puede devolver una tarjeta o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM cards WHERE account_id = ?", (cuenta_id,))
            card = cursor.fetchone()
            conn.commit()
            conn.close()
            return card
        except:
            print("Algo salió mal al buscar la tarjeta")
            conn.rollback()
            conn.close()
            return []

    ## TRANSACCIONES

    def obtenerUltimasCuatroTransaccionesDeUsuario(): # puede devolver una lista de transacciones o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT * 
                           FROM transactions 
                           WHERE cuenta_id IN (SELECT iban FROM accounts WHERE usuario_id = ?)
                           ORDER BY fecha DESC LIMIT 4
                           """,(LocalDbConn.actualUser.dni,))
            transactions = cursor.fetchall()
            conn.commit()
            conn.close()
            return transactions
        except:
            print("Algo salió mal al buscar las transacciones")
            conn.rollback()
            conn.close()

    def obtenerTodastransaccionesDeUsuario(): # puede devolver una lista de transacciones o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT * 
                           FROM transactions 
                           WHERE cuenta_id IN (SELECT iban FROM accounts WHERE usuario_id = ?)
                           ORDER BY fecha DESC
                           """,(LocalDbConn.actualUser.dni,))
            transactions = cursor.fetchall()
            conn.commit()
            conn.close()
            return transactions
        except:
            print("Algo salió mal al buscar las transacciones")
            conn.rollback()

    ## SUSCRIPCIONES

    def obtenerUltimasCuatroSuscripcionesDeUsuario(): # puede devolver una lista de suscripciones o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT * 
                           FROM subscriptions 
                           WHERE account_id = ?
                           ORDER BY fecha_renovacion DESC Limit 4
                           """,(LocalDbConn.actualUser.dni,))
            transactions = cursor.fetchall()
            conn.commit()
            conn.close()
            return transactions
        except:
            print("Algo salió mal al buscar las transacciones")
            conn.rollback()
            conn.close()

    def obtenerTodasSuscripcionesDeUsuario(): # puede devokver una lista de suscripciones o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           SELECT * 
                           FROM subscriptions 
                           WHERE account_id = ?
                           ORDER BY fecha_renovacion DESC
                           """,(LocalDbConn.actualUser.dni,))
            transactions = cursor.fetchall()
            conn.commit()
            conn.close()
            return transactions
        except Exception as e:
            print(f"Algo salió mal al buscar las transacciones: {e}")
            conn.rollback()
            conn.close()

    ## PRESTAMOS

    def insertarPrestamo(prestamoToInsert:Prestamo):
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO loans (id, usuario_id, monto, tasa_interes, plazo_meses, estado, fecha_solicitud) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(prestamoToInsert.id), 
                prestamoToInsert.usuario_id, 
                prestamoToInsert.monto, 
                prestamoToInsert.tasa_interes, 
                prestamoToInsert.plazo_meses, 
                prestamoToInsert.estado, 
                prestamoToInsert.fecha_solicitud
            ))
            conn.commit()
        except Exception as e:
            print(f"Algo salió mal al insertar el prestamo: {e}")
            conn.rollback()
        conn.close()

    def obtenerTodosLosPrestamosDeUsuario(): # puede devolver una lista de prestamos o None
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM loans WHERE usuario_id = ?", (LocalDbConn.actualUser.dni,))
            loans = cursor.fetchall()
            conn.commit()
            conn.close()
            return loans
        except:
            print("Algo salió mal al buscar los prestamos")
            conn.rollback()
            conn.close()
    
    def pagarPrestamo(monto: float, id: str): # tienes que pasarle el nuevo monto, hay que comporbar si es un pagar o delete en la ui
        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            UPDATE loans 
            SET monto = ?
            WHERE id = ?
            """, (monto, id))
            conn.commit()
        except:
            print("Algo salió mal al modificar el prestamo")
            conn.rollback()

    def borrarPrestamo(id): # si el monto que se paga es mayor o igual al monto del prestamo, se borra

        conn = LocalDbConn.conn()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM loans WHERE id = ?", (id,))
            conn.commit()
        except:
            print("Algo salió mal al borrar el prestamo")
            conn.rollback()
        conn.close()
