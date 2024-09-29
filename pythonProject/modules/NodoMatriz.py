from modules.NodoPaso import ListaPasos


class NodoMatriz:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.abajo = None


class Matriz:
    def __init__(self):
        self.cabeza = None
        self.pasos = ListaPasos()  # Agregar este atributo para almacenar los pasos

    def agregar_fila(self):
        nueva_fila = NodoMatriz(None)
        if not self.cabeza:
            self.cabeza = nueva_fila
        else:
            actual = self.cabeza
            while actual.abajo:
                actual = actual.abajo
            actual.abajo = nueva_fila
        return nueva_fila

    def agregar_columna(self, fila, dato):
        nuevo_nodo = NodoMatriz(dato)
        if not fila.siguiente:
            fila.siguiente = nuevo_nodo
        else:
            actual = fila.siguiente
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.pasos.agregar(self.pasos.contar(), dato)  # Usar el método contar

    def imprimir(self):
        actual_fila = self.cabeza
        while actual_fila:
            actual_columna = actual_fila.siguiente
            while actual_columna:
                print(f"{actual_columna.dato:18}", end=" | ")
                actual_columna = actual_columna.siguiente
            print()
            actual_fila = actual_fila.abajo
