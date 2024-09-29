class NodoPaso:
    def __init__(self, linea, componente):
        self.linea = linea
        self.componente = componente
        self.siguiente = None


class ListaPasos:
    def __init__(self):
        self.cabeza = None

    def agregar(self, linea, componente):
        nuevo_paso = NodoPaso(linea, componente)
        if not self.cabeza:
            self.cabeza = nuevo_paso
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_paso

    def imprimir(self):
        actual = self.cabeza
        while actual:
            print(f"Línea: {actual.linea}, Componente: {actual.componente}")
            actual = actual.siguiente
        print()

    def esta_vacia(self):
        return self.cabeza is None

    def desencolar(self):
        if self.cabeza is None:
            return None
        dato = self.cabeza
        self.cabeza = self.cabeza.siguiente
        return dato

    def contar(self):
        contador = 0
        actual = self.cabeza
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador
