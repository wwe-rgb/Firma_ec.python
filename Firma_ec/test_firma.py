from pyhanko.sign import signers
from pyhanko.pdf_utils.writer import PdfFileWriter
from pyhanko.pdf_utils.reader import PdfFileReader

signer= signers.SimpleSigner.load_pkcs12(
    pcks12_file= "ruta/a/tu/firma.p12",
    passphrase='b tu_contraseña_aqui'
)
with open('documento_a_firmar.pdf','rb') as doc_in:
    with open('documento_firmado.pdf', 'wb' ) as doc_ouit:
        print("PDF firmado con exito")