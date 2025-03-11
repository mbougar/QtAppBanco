from fpdf import FPDF
import sqlite3
import os
import local_db_con
import utils

# Definir rutas
diractual = os.getcwd()
path = os.path.join(diractual, "report")
logo_path = os.path.join(path, "logo.png")
arial_font_path = utils.resource_path("assets/ARIAL.TTF")  # Ruta a la fuente Arial

class PDFBase(FPDF):
    def header(self):
        self.image(utils.resource_path("assets/bancoFondo.png"), 10, 8, 33)
        self.set_font("ArialUnicode", "", 12)  # Usamos la fuente registrada
        self.cell(80)
        self.cell(30, 10, self.title, 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("ArialUnicode", "", 10)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

# Función para obtener datos de la base de datos
def fetch_data(query):
    conn = local_db_con.LocalDbConn.conn()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Función para generar reportes
def generate_report(filename, title, query, format_row):
    pdf = PDFBase()
    pdf.title = title
    pdf.add_font("ArialUnicode", "", arial_font_path, uni=True)  # Registrar fuente
    pdf.set_font("ArialUnicode", "", 12)  # Usar la fuente con soporte Unicode
    pdf.add_page()

    data = fetch_data(query)
    for row in data:
        pdf.cell(0, 10, format_row(row), 0, 1)

    pdf.output(filename)

# Reportes específicos
def generate_posicion_global():
    query = """
        SELECT u.dni, u.nombre, a.iban, c.numero, a.saldo
        FROM accounts a
        JOIN users u ON a.usuario_id = u.dni
        JOIN cards c ON c.account_id = a.iban;
    """
    generate_report("posicion_global.pdf", "Posición Global", query, 
        lambda row: f"Usuario: {row[0]} - Nombre: {row[1]} - Cuenta: {row[2]} - Tarjeta: {row[3]} - Saldo: {row[4]}€")

def generate_ultimos_movimientos():
    query = "SELECT * FROM transactions ORDER BY fecha DESC LIMIT 4;"
    generate_report("ultimos_movimientos.pdf", "Últimos Movimientos", query, 
        lambda row: f"{row[1]} - {row[2]}€ - {row[3]}")

def generate_prestamos():
    query = "SELECT * FROM loans"
    generate_report("prestamos.pdf", "Préstamos", query, 
        lambda row: f"Usuario: {row[1]} - Monto: {row[2]}€ - Estado: {row[3]}")

def generate_transacciones():
    query = "SELECT * FROM transactions;"
    generate_report("transacciones.pdf", "Transacciones", query, 
        lambda row: f"{row[1]} - {row[2]}€ - {row[3]}")

def generate_subscripciones():
    query = "SELECT * FROM subscriptions"
    generate_report("subscripciones.pdf", "Subscripciones", query, 
        lambda row: f"{row[1]} - {row[2]}€ - {row[3]}")

# Función principal
def main():
    generate_posicion_global()
    generate_ultimos_movimientos()
    generate_prestamos()
    generate_transacciones()
    generate_subscripciones()
    print("Informes generados correctamente.")

if __name__ == "__main__":
    main()
