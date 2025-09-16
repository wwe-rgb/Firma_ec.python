import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from datetime import date

# Importamos nuestras clases personalizadas
from cert_handler import ImportarCertificado
from pdf_handler import ImportarPDF
from exporter import ExportarPDF

class GUI(tk.Tk):
    """
    Crea y gestiona la interfaz gráfica de usuario (GUI) para la aplicación.
    """
    def __init__(self):
        super().__init__()
        self.title("Firmador de PDF v1.0")
        self.geometry("600x450")

        # Instancias de nuestras clases de lógica
        self.cert = ImportarCertificado()
        self.pdf = ImportarPDF()
        self.exporter = ExportarPDF()

        # --- Widgets de la Interfaz ---
        # Certificado
        self.btn_cert = tk.Button(self, text="1. Seleccionar Certificado (.p12)", command=self.seleccionar_certificado)
        self.btn_cert.pack(pady=10, padx=20, fill=tk.X)
        self.lbl_cert = tk.Label(self, text="No seleccionado", fg="red")
        self.lbl_cert.pack()
        
        tk.Label(self, text="Contraseña del Certificado:").pack(pady=(10, 0))
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack(pady=5, padx=20, fill=tk.X)

        # PDF
        self.btn_pdf = tk.Button(self, text="2. Seleccionar PDF a Firmar", command=self.seleccionar_pdf)
        self.btn_pdf.pack(pady=10, padx=20, fill=tk.X)
        self.lbl_pdf = tk.Label(self, text="No seleccionado", fg="red")
        self.lbl_pdf.pack()

        # Fecha
        tk.Label(self, text="3. Seleccionar Fecha de Firma:").pack(pady=(10, 0))
        self.cal = DateEntry(self, selectmode='day', year=date.today().year, month=date.today().month, day=date.today().day,
                       date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=5)
        
        # Botón de acción
        self.btn_firmar = tk.Button(self, text="4. Firmar y Exportar PDF", bg="green", fg="white", font=("Helvetica", 12, "bold"), command=self.firmar_y_exportar)
        self.btn_firmar.pack(pady=20, padx=20, fill=tk.X, ipady=10)

        # Etiqueta de estado
        self.lbl_status = tk.Label(self, text="Listo para firmar.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def seleccionar_certificado(self):
        path = filedialog.askopenfilename(
            title="Seleccione su certificado",
            filetypes=[("Archivos P12", "*.p12")]
        )
        if path:
            self.cert.path = path
            self.lbl_cert.config(text=path.split('/')[-1], fg="green")
            self.lbl_status.config(text=f"Certificado '{path.split('/')[-1]}' cargado.")

    def seleccionar_pdf(self):
        path = filedialog.askopenfilename(
            title="Seleccione el PDF a firmar",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if path:
            self.pdf.input_path = path
            self.lbl_pdf.config(text=path.split('/')[-1], fg="green")
            self.lbl_status.config(text=f"PDF '{path.split('/')[-1]}' listo para ser firmado.")

    def firmar_y_exportar(self):
        # Validaciones
        password = self.entry_pass.get()
        if not self.cert.path or not self.pdf.input_path or not password:
            messagebox.showerror("Error", "Por favor, seleccione el certificado, el PDF e ingrese la contraseña.")
            return

        # Pedir ubicación para guardar el archivo firmado
        output_path = filedialog.asksaveasfilename(
            title="Guardar PDF Firmado como...",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if not output_path:
            self.lbl_status.config(text="Operación cancelada por el usuario.")
            return

        # Actualizar los manejadores con toda la info
        self.cert.set_credentials(self.cert.path, password)
        self.pdf.set_paths(self.pdf.input_path, output_path)
        
        self.lbl_status.config(text="Firmando, por favor espere...")
        self.update() # Forzar actualización de la GUI

        # Llamar al exportador
        fecha_seleccionada = self.cal.get_date().strftime('%Y-%m-%d')
        resultado = self.exporter.exportar_firmado(self.cert, self.pdf, fecha_seleccionada)
        
        # Mostrar resultado
        self.lbl_status.config(text=resultado)
        if "¡Éxito!" in resultado:
            messagebox.showinfo("Proceso Completado", resultado)
        else:
            messagebox.showerror("Error en la Firma", resultado)