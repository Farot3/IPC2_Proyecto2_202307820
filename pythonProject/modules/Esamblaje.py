from modules.Cola import Cola


class PasoSimulacion:
    def __init__(self, tiempo, acciones):
        self.tiempo = tiempo
        self.acciones = acciones


class ResultadoSimulacion:
    def __init__(self, tiempo_total, pasos):
        self.tiempo_total = tiempo_total
        self.pasos = pasos


class Simulador:
    @staticmethod
    def simular_ensamblaje(maquina, producto):
        print(f"Simulando ensamblaje de {producto.nombre} en {maquina.nombre_maquina}")

        pasos = producto.elaboracion.split()
        total_tiempo = 0
        lineas = int(maquina.cantidad_lineas)
        componentes = int(maquina.cantidad_componentes)
        tiempo_ensamblaje = int(maquina.tiempo_ensamblaje)

        lineas_ensamblaje = Cola()
        for _ in range(lineas):
            lineas_ensamblaje.encolar({"posicion": 0, "ensamblando": False})

        salida = Cola()

        while pasos:
            segundo_actual = salida.frente.dato.tiempo + 1 if salida.frente else 1
            acciones = Cola()
            acciones.encolar(f"{segundo_actual}o. Segundo")

            for _ in range(lineas):
                acciones.encolar("No hacer nada")

            linea_actual = lineas_ensamblaje.frente
            indice = 1
            while linea_actual:
                if linea_actual.dato["ensamblando"]:
                    linea_actual.dato["ensamblando"] = False
                    Simulador._actualizar_accion(
                        acciones,
                        indice,
                        f"Ensamblar - Componente {linea_actual.dato['posicion']}",
                    )
                elif pasos:
                    paso = pasos[0]
                    # Aquí procesamos el paso como una cadena de texto
                    if isinstance(paso, str):
                        Simulador._actualizar_accion(
                            acciones,
                            indice,
                            f"Mover brazo - {paso}",
                        )
                        pasos.pop(0)

                linea_actual = linea_actual.siguiente
                indice += 1

            salida.encolar(PasoSimulacion(segundo_actual, acciones))
            total_tiempo += 1

        # Imprimir el resultado en consola
        print(
            f"El producto {producto.nombre} se puede elaborar óptimamente en {total_tiempo} segundos."
        )
        nodo_actual = salida.frente
        while nodo_actual:
            acciones = nodo_actual.dato.acciones
            accion_actual = acciones.frente
            while accion_actual:
                print(accion_actual.dato, end=" | ")
                accion_actual = accion_actual.siguiente
            print()
            nodo_actual = nodo_actual.siguiente

        return ResultadoSimulacion(total_tiempo, salida)

    @staticmethod
    def _actualizar_accion(cola_acciones, indice, nueva_accion):
        actual = cola_acciones.frente
        for _ in range(indice):
            if actual.siguiente:
                actual = actual.siguiente
            else:
                break
        if actual:
            actual.dato = nueva_accion
