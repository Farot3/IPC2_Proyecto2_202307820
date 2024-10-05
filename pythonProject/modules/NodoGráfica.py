class NodoGrafica:
    def __init__(self, nombre_producto, grafica_html):
        self.nombre_producto = nombre_producto
        self.grafica_html = grafica_html
        self.siguiente = None


class ListaGraficas:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre_producto, grafica_html):
        nuevo_nodo = NodoGrafica(nombre_producto, grafica_html)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_todas(self):
        actual = self.cabeza
        while actual:
            yield actual
            actual = actual.siguiente
