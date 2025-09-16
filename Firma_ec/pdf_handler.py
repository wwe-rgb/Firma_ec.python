class ImportarPDF:
    """
    Clase que funciona como un contenedor de datos para la ruta
    del PDF de entrada (original) y el de salida (firmado).
    """
    def __init__(self):
        self.input_path = ""
        self.output_path = ""

    def set_paths(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        print(f"PDF de entrada: {self.input_path}")
        print(f"PDF de salida: {self.output_path}")