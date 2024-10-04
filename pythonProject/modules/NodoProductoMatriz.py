class NodoProductoMatriz:
    def __init__(self, producto, matriz):
        self.producto = producto
        self.matriz = matriz
        self.siguiente = None


class ListaProductoMatriz:
    def __init__(self):
        self.cabeza = None

    def agregar(self, producto, matriz):
        nuevo_nodo = NodoProductoMatriz(producto, matriz)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_por_nombre(self, nombre):
        actual = self.cabeza
        while actual is not None:
            if actual.producto.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None
