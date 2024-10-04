class NodoElaboracion:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self._elaboracion = elaboracion
        self.siguiente = None

    @property
    def elaboracion(self):
        return self._elaboracion.replace(" ", "")

    @elaboracion.setter
    def elaboracion(self, value):
        self._elaboracion = value


class ListaElaboracionNodos:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def agregar(self, nombre, elaboracion):
        nuevo_nodo = NodoElaboracion(nombre, elaboracion)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamano += 1
        print(f"Elaboracion agregada: Producto: {nombre}, Elaboracion: {elaboracion}")

    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(f"Producto: {actual.nombre}, Elaboracion: {actual.elaboracion}")
            actual = actual.siguiente
