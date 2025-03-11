from fpdf import FPDF
import sqlite3
import os

diractual = os.getcwd()
path = os.path.join(diractual, "report")
logo_path = os.path.join(path, "logo.png")

class PDFBase(FPDF):
    def header(self):
        self.image(logo_path, 10, 8, 33)
        self.set_font("Arial", "B", 15)
        self.cell(80)
        self.cell(30, 10, self.title, 0, 1, "C")
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def fetch_data(query):
    conn = sqlite3.connect("banco.db")  # Asegúrate de que la ruta a tu DB es correcta
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def generate_posicion_global():
    pdf = PDFBase()
    pdf.title = "Posición Global"
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    query = """
        SELECT u.dni, a.iban, c.numero, a.saldo
        FROM accounts a
        JOIN users u ON a.usuario_id = u.dni
        JOIN cards c ON c.account_id = a.iban;
        """
    data = fetch_data(query)
    for row in data:
        pdf.cell(0, 10, f"Usuario: {row[0]} - Cuenta: {row[1]} - Tarjeta: {row[2]} - Saldo: {row[3]}€", 0, 1)
    pdf.output("posicion_global.pdf")

def generate_ultimos_movimientos():
    pdf = PDFBase()
    pdf.title = "Últimos Movimientos"
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    query = "SELECT * FROM transactions ORDER BY fecha DESC LIMIT 4;"
    data = fetch_data(query)
    for row in data:
        pdf.cell(0, 10, f"{row[1]} - {row[2]}€ - {row[3]}", 0, 1)
    pdf.output("ultimos_movimientos.pdf")

def generate_prestamos():
    pdf = PDFBase()
    pdf.title = "Préstamos"
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    query = "SELECT * FROM loans"
    data = fetch_data(query)
    for row in data:
        pdf.cell(0, 10, f"Usuario: {row[1]} - Monto: {row[2]}€ - Estado: {row[3]}", 0, 1)
    pdf.output("prestamos.pdf")

def generate_transacciones():
    pdf = PDFBase()
    pdf.title = "Transacciones"
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    query = "SELECT * FROM transactions;"
    data = fetch_data(query)
    for row in data:
        pdf.cell(0, 10, f"{row[1]} - {row[2]}€ - {row[3]}", 0, 1)
    pdf.output("transacciones.pdf")

def generate_subscripciones():
    pdf = PDFBase()
    pdf.title = "Subscripciones"
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    query = "SELECT * FROM subscriptions"
    data = fetch_data(query)
    for row in data:
        pdf.cell(0, 10, f"{row[1]} - {row[2]}€ - {row[3]}", 0, 1)
    pdf.output("subscripciones.pdf")

def main():
    generate_posicion_global()
    generate_ultimos_movimientos()
    generate_prestamos()
    generate_transacciones()
    generate_subscripciones()
    print("Informes generados correctamente.")

if __name__ == "__main__":
    main()
