class NodoLinea:
    def __init__(self, componentes, tiempoEnsamblaje, ensamblado, pos, id, secuencia):
        self.siguiente = None
        self.componentes = componentes
        self.tiempoEnsamblaje = tiempoEnsamblaje
        self.ensamblado = ensamblado
        self.pos = pos
        self.id = id
        self.secuencia = secuencia

    def agregarSecuencia(self, secuencia):
        self.secuencia = secuencia

    def moverAdelante(self):
        self.pos += 1

    def moverAtras(self):
        self.pos -= 1

    def ensamblar(self):
        self.ensamblado = True

    def __str__(self):
        return f"ID: {self.id}, Componentes: {self.componentes}, Tiempo de Ensamblaje: {self.tiempoEnsamblaje}, Ensamblado: {self.ensamblado}, Posición: {self.pos}, Secuencia: {self.secuencia}"


class ListaLineas:

    linea = 1

    def __init__(self):
        self.cabeza = None
        self.noLineas = 0
        self.tiempoEnsamblaje = 0
        self.nombreMaquina = ""

    def set_nombre_maquina(self, nombre):
        self.nombreMaquina = nombre

    def get_nombre_maquina(self):
        return self.nombreMaquina

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, componentes, tiempoEnsamblaje):
        nuevo_NodoLinea = NodoLinea(
            componentes, tiempoEnsamblaje, False, 0, self.linea, None
        )
        if self.esta_vacia():
            self.cabeza = nuevo_NodoLinea
            self.linea += 1
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_NodoLinea
            self.linea += 1

    def obtener(self, pos):
        if self.esta_vacia():
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
            print(actual)
            actual = actual.siguiente
