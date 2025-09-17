# logic.py

from datetime import datetime
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec, append_signature_field

class ImportarCertificado:
    """Contenedor de datos para el certificado .p12 y su contraseña."""
    def __init__(self):
        self.path = ""
        self.password = ""

    def set_credentials(self, path, password):
        self.path = path
        self.password = password

class ImportarPDF:
    """Contenedor de datos para las rutas del PDF."""
    def __init__(self):
        self.input_path = ""
        self.output_path = ""

    def set_paths(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

class FirmarPDF:
    """Lógica principal para aplicar la firma digital a un PDF."""
    def sign(self, p12_path, password, pdf_input_path, pdf_output_path, sign_datetime):
        try:
            firmante = signers.SimpleSigner.load_pkcs12(
                p12_path, passphrase=password.encode('utf-8')
            )
            with open(pdf_input_path, 'rb') as doc_in, open(pdf_output_path, 'wb') as doc_out:
                writer = IncrementalPdfFileWriter(doc_in)
                append_signature_field(
                    writer,
                    SigFieldSpec(sig_field_name='Signature1', box=(50, 50, 250, 100))
                )
                signers.sign_pdf(
                    writer,
                    signers.PdfSignatureMetadata(field_name='Signature1'), 
                    signer=firmante,
                    output=doc_out
                )
            return f"¡Éxito! PDF guardado en:\n{pdf_output_path}"
        except Exception as e:
            return f"Error: {e}"

class ExportarPDF:
    """Orquesta el proceso de firma."""
    def __init__(self):
        self.firmador = FirmarPDF()

    def exportar_firmado(self, cert_handler, pdf_handler, fecha_obj):
        return self.firmador.sign(
            p12_path=cert_handler.path,
            password=cert_handler.password,
            pdf_input_path=pdf_handler.input_path,
            pdf_output_path=pdf_handler.output_path,
            sign_datetime=fecha_obj
        )