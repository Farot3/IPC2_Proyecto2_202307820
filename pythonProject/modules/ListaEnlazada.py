from modules.NodoSimulacion import Nodo


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    def obtener(self, indice):
        actual = self.cabeza
        for _ in range(indice):
            if actual:
                actual = actual.siguiente
            else:
                return None
        return actual.dato if actual else None
