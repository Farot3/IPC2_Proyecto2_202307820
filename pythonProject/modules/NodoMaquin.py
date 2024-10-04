class NodoMaquina:
    def __init__(
        self, nombre, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje
    ):
        self.nombre = nombre
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.siguiente = None

    def __str__(self):
        return f"Maquina: {self.nombre}, Lineas: {self.cantidad_lineas}, Componentes: {self.cantidad_componentes}, Tiempo de Ensamblaje: {self.tiempo_ensamblaje}"


class ListaMaquinas:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def agregar(self, nombre, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje):
        nuevo_nodo = NodoMaquina(
            nombre, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje
        )
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamano += 1

    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual)
            actual = actual.siguiente
