class NodoNombre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None


class ListaNombres:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre):
        nuevo_nodo = NodoNombre(nombre)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.nombre
            actual = actual.siguiente


class NodoMaquina:
    def __init__(self, maquina, productos):
        self.siguiente = None
        self.maquina = maquina
        self.productos = productos
        print(
            f"Creado NodoMaquina: {self.maquina.get_nombre_maquina()}, Productos: {self.productos}"
        )


class ListaMaquina:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, maquina, productos):
        nuevo_NodoMaquina = NodoMaquina(maquina, productos)
        if self.esta_vacia():
            self.cabeza = nuevo_NodoMaquina
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_NodoMaquina
        self.tamano += 1

    def obtener_por_nombre(self, nombre):
        actual = self.cabeza
        while actual is not None:
            if actual.maquina.get_nombre_maquina() == nombre:  # Usar get_nombre_maquina
                return actual
            actual = actual.siguiente
        return None

    def obtener_por_indice(self, indice):
        if indice < 0 or indice >= self.tamano:
            return None
        actual = self.cabeza
        for i in range(indice):
            actual = actual.siguiente
        return actual

    def mostrar(self):
        actual = self.cabeza
        while actual is not None:
            print(actual.maquina.nombre)
            print(actual.productos)
            actual = actual.siguiente

    def borrar_todos(self):
        self.cabeza = None
        self.tamano = 0

    def obtener_nombres_maquinas(self):
        nombres = ListaNombres()
        actual = self.cabeza
        while actual is not None:
            nombres.agregar(
                actual.maquina.get_nombre_maquina()
            )  # Usar get_nombre_maquina
            actual = actual.siguiente
        return nombres

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual
            actual = actual.siguiente
