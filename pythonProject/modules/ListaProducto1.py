class NodoInstrucciones:
    def __init__(self, valor, valor2):
        self.valor = valor
        self.valor2 = valor2
        self.siguiente = None
        self.nombre = ""


class NodoNombreProducto:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None


class ListaNombresProductos:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre):
        nuevo_nodo = NodoNombreProducto(nombre)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.nombre
            actual = actual.siguiente


class NodoInformacionProducto:
    def __init__(self, nombre, valor, valor2):
        self.nombre = nombre
        self.valor = valor
        self.valor2 = valor2
        self.siguiente = None


class ListaInformacionProductos:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre, valor, valor2):
        nuevo_nodo = NodoInformacionProducto(nombre, valor, valor2)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual
            actual = actual.siguiente


class ListaProductos:
    def __init__(self):
        self.cabeza = None
        self.nombreMaquina = ""
        self.tamano = 0

    def agregar(self, valor, nombre, valor2):
        nuevo_NodoInstrucciones = NodoInstrucciones(valor, valor2)
        nuevo_NodoInstrucciones.nombre = nombre
        print(f"Agregando producto con nombre: {nombre}")
        if self.cabeza is None:
            self.cabeza = nuevo_NodoInstrucciones
            self.cabeza.nombre = nombre
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_NodoInstrucciones

        self.tamano += 1

    def obtener(self, pos):
        if self.cabeza is None:
            return None
        actual = self.cabeza
        for i in range(pos):
            if actual.siguiente is None:
                return None
            actual = actual.siguiente
        return actual

    def mostrar(self):
        actual = self.cabeza
        while actual is not None:
            print(actual.valor)
            actual = actual.siguiente

    def buscar(self, valor):
        actual = self.cabeza
        while actual is not None:
            if actual.valor == valor:
                return valor
            actual = actual.siguiente
        return None

    def eliminar_todo(self):
        self.cabeza = None

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual
            actual = actual.siguiente

    def obtener_informacion_detallada(self):
        informacion = ListaInformacionProductos()
        actual = self.cabeza
        while actual is not None:
            informacion.agregar(actual.nombre, actual.valor, actual.valor2)
            actual = actual.siguiente
        return informacion

    def obtener_nombres_productos(self):
        nombres = ListaNombresProductos()
        actual = self.cabeza
        while actual is not None:
            nombres.agregar(actual.nombre)
            actual = actual.siguiente
        return nombres
