class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.nombre = ""
        self.siguiente = None

class ListaSimple:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0
        self.nombre = ""

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamano += 1

    def obtener(self, pos):
        if self.esta_vacia():
            return None
        actual = self.cabeza
        for i in range(pos):
            if actual.siguiente is None:
                return None
            actual = actual.siguiente
        return actual.dato

    def mostrar(self):
        actual = self.cabeza
        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente
    
    def buscar(self, dato):
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                return dato
            actual = actual.siguiente
        return None
    
    def eliminar_todo(self):
        self.cabeza = None
        
