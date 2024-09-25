import xml.etree.ElementTree as ET
from modules.NodoMaquina import NodoMaquina
from modules.NodoProducto import NodoProducto


class ListaMaquina:
    def __init__(self):
        self.cabeza = None

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual
            actual = actual.siguiente

    def agregar(self, nodo):
        if not self.cabeza:
            self.cabeza = self.cola = nodo
        else:
            nodo.anterior = self.cola
            self.cola.siguiente = nodo
            self.cola = nodo

    def buscar_maquina(self, nombre_maquina):
        actual = self.cabeza
        while actual:
            if (
                isinstance(actual, NodoMaquina)
                and actual.NombreMaquina == nombre_maquina
            ):
                return actual
            actual = actual.siguiente
        return None

    def imprimir(self):
        actual = self.cabeza
        while actual:
            if isinstance(actual, NodoMaquina):
                print(f"Máquina: {actual.NombreMaquina}")
                print(f"  Líneas de producción: {actual.CantidadLineas}")
                print(f"  Componentes: {actual.CantidadComponentes}")
                print(f"  Tiempo de ensamblaje: {actual.TiempoEnsamblaje}")
                print("  Productos:")
                producto = actual.productos
                while producto:
                    print(
                        f"    - {producto.nombre} (Elaborado por: {producto.elaboracion})"
                    )
                    producto = producto.siguiente
            actual = actual.siguiente
        print()


def leer_maquina(archivo_xml):
    tree = ET.ElementTree(ET.fromstring(archivo_xml))
    root = tree.getroot()

    lista_maquinas = ListaMaquina()

    for maquina in root.findall("Maquina"):
        nombre_maquina = maquina.find("NombreMaquina").text.strip()
        cantidad_lineas = maquina.find("CantidadLineasProduccion").text.strip()
        cantidad_componentes = maquina.find("CantidadComponentes").text.strip()
        tiempo_ensamblaje = maquina.find("TiempoEnsamblaje").text.strip()

        nodo_maquina = NodoMaquina(
            nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje
        )

        lista_productos = ListaMaquina()
        listado_productos = maquina.find("ListadoProductos")
        for producto in listado_productos.findall("Producto"):
            nombre_producto = producto.find("nombre").text.strip()
            elaboracion = producto.find("elaboracion").text.strip()
            lista_productos.agregar(NodoProducto(nombre_producto, elaboracion))

        nodo_maquina.productos = lista_productos.cabeza
        lista_maquinas.agregar(nodo_maquina)

    return lista_maquinas
