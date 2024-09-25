from modules.ListaProducto import ListaProducto


class NodoMaquinaConProductos:
    def __init__(
        self, nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje
    ):
        self.nombre_maquina = nombre_maquina
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.productos = ListaProducto()
        self.siguiente = None
