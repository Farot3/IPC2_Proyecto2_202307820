class NodoComponente:
    def __init__(self, componente):
        self.componente = componente
        self.siguiente = None

    def __str__(self):
        return f"Componente: {self.componente}"


class ListaComponentes:
    def __init__(self):
        self.cabeza = None

    def agregar(self, componente):
        nuevo_nodo = NodoComponente(componente)
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
            yield actual.componente
            actual = actual.siguiente

    def mostrar(self):
        actual = self.cabeza
        while actual is not None:
            print(actual)
            actual = actual.siguiente
