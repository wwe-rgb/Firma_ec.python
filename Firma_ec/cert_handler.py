class ImportarCertificado:
    """
    Clase que funciona como un contenedor de datos para la ruta
    del certificado .p12 y su contraseña. La selección real del
    archivo se gestionará en la GUI.
    """
    def __init__(self):
        self.path = ""
        self.password = ""

    def set_credentials(self, path, password):
        self.path = path
        self.password = password
        print(f"Certificado seleccionado: {self.path}")