from modules.NodoPaso import ListaPasos


class NodoProducto:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self.elaboracion = elaboracion
        self.pasos = ListaPasos()
        self.siguiente = None
        self.anterior = None
        self._procesar_elaboracion()

    def _procesar_elaboracion(self):
        import re

        matches = re.findall(r"L(\d+)C(\d+)", self.elaboracion)
        for match in matches:
            linea, componente = map(int, match)
            self.pasos.agregar(linea, componente)
