class Nodo:
    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None


class ListaNodosSecuencia:
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

    def eliminar(self, valor):
        actual = self.cabeza
        anterior = None
        while actual and actual.valor != valor:
            anterior = actual
            actual = actual.siguiente
        if actual:
            if anterior:
                anterior.siguiente = actual.siguiente
            else:
                self.cabeza = actual.siguiente

    def obtener_todos(self):
        valores = ListaNodosSecuencia()
        actual = self.cabeza
        while actual:
            valores.agregar(actual.valor)
            actual = actual.siguiente
        return valores

    def esta_vacia(self):
        return self.cabeza is None

    def __str__(self):
        actual = self.cabeza
        resultado = ""
        while actual:
            resultado += actual.valor
            if actual.siguiente:
                resultado += ", "
            actual = actual.siguiente
        return resultado

    def __iter__(self):
        self._iter_node = self.cabeza
        return self

    def __next__(self):
        if self._iter_node:
            valor = self._iter_node.valor
            self._iter_node = self._iter_node.siguiente
            return valor
        else:
            raise StopIteration
