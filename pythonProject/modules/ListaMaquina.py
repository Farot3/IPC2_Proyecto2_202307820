import xml.etree.ElementTree as ET
from modules.NodoMaquina import NodoMaquinaConProductos
from modules.NodoProducto import NodoProducto


class ListaMaquina:
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

    def buscar_maquina(self, nombre_maquina):
        actual = self.cabeza
        while actual:
            if actual.nombre_maquina == nombre_maquina:
                return actual
            actual = actual.siguiente
        return None

    def imprimir(self):
        actual = self.cabeza
        while actual:
            print(f"Máquina: {actual.nombre_maquina}")
            print(f"  Líneas de producción: {actual.cantidad_lineas}")
            print(f"  Componentes: {actual.cantidad_componentes}")
            print(f"  Tiempo de ensamblaje: {actual.tiempo_ensamblaje}")
            print("  Productos:")
            actual.productos.imprimir()
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


def leer_maquina(archivo_xml, lista_maquinas):
    tree = ET.ElementTree(ET.fromstring(archivo_xml))
    root = tree.getroot()

    for maquina in root.findall("Maquina"):
        nombre_maquina = maquina.find("NombreMaquina").text.strip()
        cantidad_lineas = maquina.find("CantidadLineasProduccion").text.strip()
        cantidad_componentes = maquina.find("CantidadComponentes").text.strip()
        tiempo_ensamblaje = maquina.find("TiempoEnsamblaje").text.strip()

        nodo_maquina = NodoMaquinaConProductos(
            nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje
        )

        listado_productos = maquina.find("ListadoProductos")
        for producto in listado_productos.findall("Producto"):
            nombre_producto = producto.find("nombre").text.strip()
            elaboracion = producto.find("elaboracion").text.strip()
            nodo_producto = NodoProducto(nombre_producto, elaboracion)
            nodo_maquina.productos.agregar(nodo_producto)

        lista_maquinas.agregar(nodo_maquina)

    print("Machines Loaded from XML:")
    lista_maquinas.imprimir()
    return lista_maquinas
