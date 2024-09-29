class LineaEnsamblaje:
    def __init__(self, num_componentes):
        self.posicion_brazo = 0
        self.tiempo_ensamblaje_restante = 0
        self.num_componentes = num_componentes

    def mover_brazo(self, destino):
        tiempo = abs(destino - self.posicion_brazo)
        self.posicion_brazo = destino
        return tiempo

    def ensamblar(self, tiempo_ensamblaje):
        self.tiempo_ensamblaje_restante = tiempo_ensamblaje

    def actualizar(self):
        if self.tiempo_ensamblaje_restante > 0:
            self.tiempo_ensamblaje_restante -= 1
            return "Ensamblando"
        return "No hacer nada"
