from modules.ListaProducto import ListaProducto
from modules.LineaEsamblaje import LineaEnsamblaje
from modules.ListaEnlazada import ListaEnlazada


class NodoMaquinaConProductos:
    def __init__(
        self, nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje
    ):
        self.nombre_maquina = nombre_maquina
        self.cantidad_lineas = int(cantidad_lineas)
        self.cantidad_componentes = int(cantidad_componentes)
        self.tiempo_ensamblaje = int(tiempo_ensamblaje)
        self.productos = ListaProducto()
        self.lineas = ListaEnlazada()
        for _ in range(self.cantidad_lineas):
            self.lineas.agregar(LineaEnsamblaje(self.cantidad_componentes))
        self.siguiente = None
