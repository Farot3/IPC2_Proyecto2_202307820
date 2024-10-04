class Nodo:
    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None
        self.abajo = None
        self.nombreProducto = ""


class Matriz:
    def __init__(self, filas, columnas, nombre):
        self.filas = filas
        self.columnas = columnas
        self.cabeza = self._crear_matriz()
        self.nombre = nombre

    def eliminar_fila(self, fila):
        if fila < 0 or fila >= self.filas:
            print("Fila inválida")
            return

        if fila == 0:
            self.cabeza = self.cabeza.abajo
        else:
            nodo_anterior = self._obtener_nodo(fila - 1, 0)
            nodo_a_eliminar = nodo_anterior.abajo

            nodo_anterior.abajo = nodo_a_eliminar.abajo

            nodo_a_eliminar.abajo = None
            nodo_a_eliminar.siguiente = None

        self.filas -= 1

    def anadir_fila(self):
        # Recorrer hasta la última fila
        nodo = self.cabeza
        while nodo.abajo is not None:
            nodo = nodo.abajo

        # Crear la nueva fila
        nueva_fila = Nodo()
        nodo.abajo = nueva_fila  # Conectar la última fila existente con la nueva fila
        nodo_columna_superior = nodo
        nodo_columna_inferior = nueva_fila

        # Crear los nodos en la nueva fila y conectarlos
        for _ in range(self.columnas - 1):
            nodo_columna_inferior.siguiente = Nodo()
            nodo_columna_inferior = nodo_columna_inferior.siguiente
            nodo_columna_superior = nodo_columna_superior.siguiente
            nodo_columna_superior.abajo = nodo_columna_inferior  # Conectar cada nodo de la columna superior con la nueva fila

        self.filas += 1

    def filas(self):
        return self.filas

    def columnas(self):
        return self.columnas

    def _crear_matriz(self):
        cabeza = Nodo()
        fila_actual = cabeza

        for _ in range(self.columnas - 1):
            fila_actual.siguiente = Nodo()
            fila_actual = fila_actual.siguiente

        nodo_fila_superior = cabeza
        for _ in range(self.filas - 1):
            nodo_fila_actual = Nodo()
            nodo_fila_superior.abajo = nodo_fila_actual
            nodo_columna_superior = nodo_fila_superior
            nodo_columna_inferior = nodo_fila_actual

            for _ in range(self.columnas):
                nodo_columna_inferior.siguiente = Nodo()
                nodo_columna_superior.abajo = nodo_columna_inferior.siguiente
                nodo_columna_superior = nodo_columna_superior.siguiente
                nodo_columna_inferior = nodo_columna_inferior.siguiente

            nodo_fila_superior = nodo_fila_superior.abajo

        return cabeza

    def establecer_valor(self, fila, columna, valor):
        nodo = self._obtener_nodo(fila, columna)
        if nodo:
            nodo.valor = valor
        else:
            print("Posición inválida")

    def adherir_valor(self, fila, columna, valor):
        nodo = self._obtener_nodo(fila, columna)
        if nodo:
            nodo.valor += valor
        else:
            print("Posición inválida")

    def obtener_valor(self, fila, columna):
        nodo = self._obtener_nodo(fila, columna)
        if nodo:
            return nodo.valor
        else:
            print(
                "Posición"
                + str(fila)
                + " "
                + str(columna)
                + " "
                + "inválida en la matriz"
            )
            return None

    def _obtener_nodo(self, fila, columna):
        if fila < 0 or columna < 0 or fila >= self.filas or columna >= self.columnas:
            return None

        actual = self.cabeza
        for _ in range(fila):
            actual = actual.abajo

        for _ in range(columna):
            actual = actual.siguiente

        return actual

    def imprimirDatos(self):
        print("Matriz: ")
        print(self.nombre)
        print(str(self.filas) + "x" + str(self.columnas))

    def imprimir_matriz(self):
        fila_actual = self.cabeza
        while fila_actual is not None:
            columna_actual = fila_actual
            while columna_actual is not None:
                valor = columna_actual.valor
                print(valor if valor is not None else "0", end=" ")
                columna_actual = columna_actual.siguiente
            print()
            fila_actual = fila_actual.abajo

        print("")
