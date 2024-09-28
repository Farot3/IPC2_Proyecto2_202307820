from modules.NodoSimulacion import Nodo


class Cola:
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.frente:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

    def desencolar(self):
        if not self.frente:
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        return dato

    def esta_vacia(self):
        return self.frente is None
