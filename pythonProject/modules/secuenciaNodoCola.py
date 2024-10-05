class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class ListaNodos:
    def __init__(self):
        self.cabeza = None

    def agregar(self, valor):
        nuevo_nodo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_todos(self):
        actual = self.cabeza
        resultado = ""
        while actual:
            if resultado:
                resultado += "-"
            resultado += actual.valor
            actual = actual.siguiente
        return resultado
