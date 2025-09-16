from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec, append_signature_field

class FirmarPDF:
    """
    Contiene la lógica principal para aplicar la firma digital
    a un documento PDF utilizando un certificado .p12.
    """
    def sign(self, p12_path, password, pdf_input_path, pdf_output_path, sign_datetime):
        try:
            # 1. Cargar el firmante desde el archivo .p12
            firmante = signers.SimpleSigner.load_pkcs12(
                p12_path, passphrase=password.encode('utf-8')
            )

            # 2. Abrir el PDF de entrada y crear un escritor para el de salida
            with open(pdf_input_path, 'rb') as doc_in, open(pdf_output_path, 'wb') as doc_out:
                writer = IncrementalPdfFileWriter(doc_in)
                
                # 3. Especificar dónde aparecerá la firma (opcional pero recomendado)
                # Aquí la ponemos en la primera página, en la esquina inferior izquierda.
                append_signature_field(
                    writer,
                    SigFieldSpec(
                        sig_field_name='Signature1',
                        box=(50, 50, 250, 100) # (x1, y1, x2, y2)
                    )
                )

                # 4. Realizar la firma
                signers.sign_pdf(
                    writer,
                    signers.PdfSignatureMetadata(
                        field_name='Signature1', 
                        signing_time=sign_datetime # Usamos la fecha seleccionada
                    ),
                    signer=firmante,
                    output=doc_out
                )
            
            return "¡Éxito! El PDF ha sido firmado correctamente."
        
        except Exception as e:
            # Capturamos cualquier error (ej. contraseña incorrecta)
            print(f"Error al firmar: {e}")
            return f"Error: {e}"