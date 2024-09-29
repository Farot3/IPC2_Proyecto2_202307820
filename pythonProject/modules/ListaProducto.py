class ListaProducto:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nodo):
        if not self.cabeza:
            self.cabeza = nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nodo

    def buscar_producto(self, nombre_producto):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre_producto:
                return actual
            actual = actual.siguiente
        return None

    def imprimir(self):
        actual = self.cabeza
        while actual:
            print(f"Producto: {actual.nombre} (Elaborado por: {actual.elaboracion})")
            print("  Pasos de elaboración:")
            actual.pasos.imprimir()
            actual = actual.siguiente
        print()

    def __iter__(self):
        self._iter_node = self.cabeza
        return self

    def __next__(self):
        if self._iter_node:
            current = self._iter_node
            self._iter_node = self._iter_node.siguiente
            return current
        else:
            raise StopIteration
