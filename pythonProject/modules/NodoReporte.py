class NodoReporte:
    def __init__(self, nombre_producto, componentes, tabla_html):
        self.nombre_producto = nombre_producto
        self.componentes = componentes
        self.tabla_html = tabla_html
        self.siguiente = None


class ListaReportes:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre_producto, componentes, tabla_html):
        nuevo_reporte = NodoReporte(nombre_producto, componentes, tabla_html)
        if self.cabeza is None:
            self.cabeza = nuevo_reporte
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_reporte

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual
            actual = actual.siguiente
