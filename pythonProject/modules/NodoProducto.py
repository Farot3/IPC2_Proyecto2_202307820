class NodoProducto:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self.elaboracion = elaboracion
        self.siguiente = None
        self.anterior = None
