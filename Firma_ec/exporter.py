from signer import FirmarPDF
from datetime import datetime

class ExportarPDF:
    """
    Clase que orquesta el proceso. Recibe los datos de los
    otros objetos y llama a la clase de firma para generar
    el archivo final.
    """
    def __init__(self):
        self.firmador = FirmarPDF()

    def exportar_firmado(self, cert_handler, pdf_handler, fecha_str):
        # Convertimos el string de fecha a un objeto datetime
        try:
            # Asumimos formato YYYY-MM-DD, y añadimos la hora actual
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').replace(
                hour=datetime.now().hour,
                minute=datetime.now().minute,
                second=datetime.now().second
            )
        except ValueError:
            return "Error: El formato de la fecha es incorrecto. Use YYYY-MM-DD."

        return self.firmador.sign(
            p12_path=cert_handler.path,
            password=cert_handler.password,
            pdf_input_path=pdf_handler.input_path,
            pdf_output_path=pdf_handler.output_path,
            sign_datetime=fecha_obj
        )