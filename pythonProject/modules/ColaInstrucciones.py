from modules.NodoComponente import ListaComponentes


class NodoInstruccion:
    def __init__(self, linea, componente):
        self.linea = linea
        self.componente = componente
        self.siguiente = None
        self.ensamblado = False

    def ensamblar(self):
        self.ensamblado = True


class Producto:
    def __init__(self, nombre, valor, valor2):
        self.nombre = nombre
        self.valor = valor  # ColaInstrucciones
        self.valor2 = valor2  # ListaComponentes

    def obtener_componentes(self):
        componentes = ListaComponentes()
        actual = self.valor.frente
        while actual:
            componentes.agregar(
                f"Línea: {actual.linea}, Componente: {actual.componente}"
            )
            actual = actual.siguiente
        return componentes


class ColaInstrucciones:
    def __init__(self):
        self.frente = None
        self.final = None
        self.nombreProducto = ""
        self.noInstrucciones = 0
        self.secuencia = None

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, linea, componente):
        nuevo_NodoInstruccion = NodoInstruccion(linea, componente)
        if self.esta_vacia():
            self.frente = self.final = nuevo_NodoInstruccion
        else:
            self.final.siguiente = nuevo_NodoInstruccion
            self.final = nuevo_NodoInstruccion

    def desencolar(self):
        if self.esta_vacia():
            return None
        linea = self.frente.linea
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        return linea

    def primeroEnsamblado(self):
        if self.esta_vacia():
            return None
        return self.frente

    def obtener_valor(self, linea):
        if self.esta_vacia():
            return None
        actual = self.frente
        while actual is not None:
            if actual.linea == linea:
                return actual.componente
            actual = actual.siguiente
        return None

    def primero(self):
        if self.esta_vacia():
            return None
        return self.frente

    def mostrar(self):
        actual = self.frente
        while actual is not None:
            print(actual)
            print("Linea: ", actual.linea, " Componente: ", actual.componente)
            actual = actual.siguiente
