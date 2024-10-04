class NodoPaso:
    def __init__(self, paso):
        self.paso = paso
        self.siguiente = None


class ListaPasos:
    def __init__(self):
        self.cabeza = None

    def agregar(self, paso):
        nuevo_nodo = NodoPaso(paso)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.paso
            actual = actual.siguiente
