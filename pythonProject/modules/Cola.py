class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamano = 0

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.frente = self.final = nuevo_nodo

        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.tamano += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        self.tamano -= 1
        if self.frente is None:
            self.final = None
        return dato

    def primero(self):
        if self.esta_vacia():
            return None
        return self.frente.dato

    def mostrar(self):
        actual = self.frente
        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente
