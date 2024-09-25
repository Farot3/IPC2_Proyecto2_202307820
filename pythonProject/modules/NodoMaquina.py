class NodoMaquina:
    def __init__(
        self, NombreMaquina, CantidadLineas, CantidadComponentes, TiempoEnsamblaje
    ):
        self.NombreMaquina = NombreMaquina
        self.CantidadLineas = CantidadLineas
        self.CantidadComponentes = CantidadComponentes
        self.TiempoEnsamblaje = TiempoEnsamblaje
        self.siguiente = None
        self.anterior = None
        self.productos = None  # Cabeza de la lista de productos
