# gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, font
from tkcalendar import DateEntry
from datetime import datetime

# Importamos las clases de lógica desde nuestro archivo logic.py
from logic import ImportarCertificado, ImportarPDF,ExportarPDF

class GUI(tk.Tk):
    """Crea y gestiona la interfaz gráfica de usuario (GUI) para la aplicación."""
    def __init__(self):
        super().__init__()

        # --- Estilos y Colores ---
        self.BG_COLOR = "#f0f0f0"
        self.FRAME_COLOR = "#ffffff"
        self.BTN_COLOR = "#2196F3"
        self.SUCCESS_COLOR = "#4CAF50"
        self.DANGER_COLOR = "#F44336"
        self.FONT_NORMAL = font.Font(family="Helvetica", size=10)
        self.FONT_BOLD = font.Font(family="Helvetica", size=11, weight="bold")

        # --- Configuración de la Ventana ---
        self.title("Firmador de PDF v2.0")
        self.geometry("550x500")
        self.resizable(False, False)
        self.config(bg=self.BG_COLOR, padx=20, pady=20)

        # Instancias de la lógica
        self.cert = ImportarCertificado()
        self.pdf = ImportarPDF()
        self.exporter = ExportarPDF()

        # --- Crear Widgets ---
        self._crear_widgets()

    def _crear_widgets(self):
        frame_cert = tk.Frame(self, bg=self.FRAME_COLOR, padx=15, pady=15)
        frame_cert.pack(fill=tk.X, pady=5)
        self.btn_cert = tk.Button(frame_cert, text="1. Seleccionar Certificado (.p12)", command=self.seleccionar_certificado, font=self.FONT_NORMAL, bg=self.BTN_COLOR, fg="white", relief=tk.FLAT, width=40)
        self.btn_cert.pack(fill=tk.X)
        self.lbl_cert = tk.Label(frame_cert, text="No seleccionado", fg=self.DANGER_COLOR, bg=self.FRAME_COLOR, font=self.FONT_NORMAL)
        self.lbl_cert.pack(pady=5)
        tk.Label(frame_cert, text="Contraseña:", bg=self.FRAME_COLOR, font=self.FONT_NORMAL).pack(pady=(10, 0))
        self.entry_pass = tk.Entry(frame_cert, show="*", font=self.FONT_NORMAL, relief=tk.SOLID, bd=1)
        self.entry_pass.pack(pady=5, fill=tk.X)

        frame_pdf = tk.Frame(self, bg=self.FRAME_COLOR, padx=15, pady=15)
        frame_pdf.pack(fill=tk.X, pady=5)
        self.btn_pdf = tk.Button(frame_pdf, text="2. Seleccionar PDF a Firmar", command=self.seleccionar_pdf, font=self.FONT_NORMAL, bg=self.BTN_COLOR, fg="white", relief=tk.FLAT)
        self.btn_pdf.pack(fill=tk.X)
        self.lbl_pdf = tk.Label(frame_pdf, text="No seleccionado", fg=self.DANGER_COLOR, bg=self.FRAME_COLOR, font=self.FONT_NORMAL)
        self.lbl_pdf.pack(pady=5)

        frame_date = tk.Frame(self, bg=self.FRAME_COLOR, padx=15, pady=15)
        frame_date.pack(fill=tk.X, pady=5)
        tk.Label(frame_date, text="3. Seleccionar Fecha de Firma:", bg=self.FRAME_COLOR, font=self.FONT_NORMAL).pack()
        self.cal = DateEntry(frame_date, selectmode='day', date_pattern='yyyy-mm-dd', font=self.FONT_NORMAL)
        self.cal.pack(pady=5)
        
        self.btn_firmar = tk.Button(self, text="Firmar y Exportar PDF", command=self.firmar_y_exportar, font=self.FONT_BOLD, bg=self.SUCCESS_COLOR, fg="white", relief=tk.FLAT, pady=10)
        self.btn_firmar.pack(pady=20, fill=tk.X)

        self.lbl_status = tk.Label(self, text="Listo para firmar.", bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=10)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def seleccionar_certificado(self):
        path = filedialog.askopenfilename(title="Seleccione su certificado", filetypes=[("Archivos P12", "*.p12")])
        if path:
            self.cert.path = path
            filename = path.split('/')[-1]
            self.lbl_cert.config(text=filename, fg=self.SUCCESS_COLOR)
            self.lbl_status.config(text=f"Certificado '{filename}' cargado.")

    def seleccionar_pdf(self):
        path = filedialog.askopenfilename(title="Seleccione el PDF a firmar", filetypes=[("Archivos PDF", "*.pdf")])
        if path:
            self.pdf.input_path = path
            filename = path.split('/')[-1]
            self.lbl_pdf.config(text=filename, fg=self.SUCCESS_COLOR)
            self.lbl_status.config(text=f"PDF '{filename}' listo para ser firmado.")

    def firmar_y_exportar(self):
        password = self.entry_pass.get()
        if not self.cert.path or not self.pdf.input_path or not password:
            messagebox.showerror("Error de Validación", "Por favor, complete todos los campos.")
            return

        output_path = filedialog.asksaveasfilename(title="Guardar PDF Firmado como...", defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if not output_path:
            self.lbl_status.config(text="Operación cancelada.")
            return

        self.cert.set_credentials(self.cert.path, password)
        self.pdf.set_paths(self.pdf.input_path, output_path)
        
        self.lbl_status.config(text="Firmando, por favor espere...")
        self.update_idletasks()

        fecha_seleccionada = self.cal.get_date()
        fecha_hora_firma = datetime.combine(fecha_seleccionada, datetime.now().time())

        resultado = self.exporter.exportar_firmado(self.cert, self.pdf, fecha_hora_firma)
        
        self.lbl_status.config(text=resultado.split('\n')[0])
        if "¡Éxito!" in resultado:
            messagebox.showinfo("Proceso Completado", resultado)
        else:
            messagebox.showerror("Error en la Firma", resultado)