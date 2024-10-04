class NodoRelacion:
    def __init__(self, nodo_producto, nodo_elaboracion):
        self.nodo_producto = nodo_producto
        self.nodo_elaboracion = nodo_elaboracion
        self.siguiente = None

    def obtener_componentes(self):
        return self.nodo_producto.valor2.obtener_componentes()


class ListaRelaciones:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nodo_producto, nodo_elaboracion):
        nuevo_nodo = NodoRelacion(nodo_producto, nodo_elaboracion)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        print(
            f"Relacion agregada: Producto: {nodo_producto.nombre}, Elaboracion: {nodo_elaboracion.elaboracion}"
        )

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual
            actual = actual.siguiente

    def mostrar(self):
        actual = self.cabeza
        while actual is not None:
            print(
                f"Producto: {actual.nodo_producto.nombre}, Elaboracion: {actual.nodo_elaboracion.elaboracion}"
            )
            actual = actual.siguiente
