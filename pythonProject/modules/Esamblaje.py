import re
from modules.NodoMatriz import Matriz
from modules.NodoPaso import ListaPasos


class Producto:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self.pasos = ListaPasos()
        matches = re.findall(r"L\d+C\d+", elaboracion)
        for match in matches:
            linea, componente = map(int, match[1:].split("C"))
            self.pasos.agregar(linea, componente)


def mover_brazo(linea, paso):
    if paso.componente > linea.posicion_brazo:
        linea.posicion_brazo += 1
    else:
        linea.posicion_brazo -= 1
    return f"Mover brazo – componente {linea.posicion_brazo}"


def iniciar_ensamblaje(linea, paso, maquina):
    linea.tiempo_ensamblaje_restante = maquina.tiempo_ensamblaje - 1
    return f"Iniciar ensamblaje C{paso.componente}"


def verificar_ensamblando(maquina):
    for i in range(maquina.cantidad_lineas):
        linea = maquina.lineas.obtener(i)
        if linea.tiempo_ensamblaje_restante > 0:
            return True
    return False


def reiniciar_maquina(maquina):
    for i in range(maquina.cantidad_lineas):
        linea = maquina.lineas.obtener(i)
        linea.posicion_brazo = 0
        linea.tiempo_ensamblaje_restante = 0
    maquina.tabla = Matriz()


class Simulador:
    @staticmethod
    def simular(maquina, producto):
        reiniciar_maquina(
            maquina
        )  # Reiniciar la máquina antes de comenzar la simulación

        tiempo_total = 0
        pasos_producto = producto.pasos

        print(f"Simulando ensamblaje de {producto.nombre} en {maquina.nombre_maquina}")
        print(
            "Tiempo | "
            + " | ".join(
                [f"Línea de ensamblaje {i+1}" for i in range(maquina.cantidad_lineas)]
            )
        )
        print("-" * (8 + 30 * maquina.cantidad_lineas))

        matriz = Matriz()

        pasos_pendientes = [ListaPasos() for _ in range(maquina.cantidad_lineas)]
        nodo_actual = pasos_producto.cabeza
        while nodo_actual:
            pasos_pendientes[nodo_actual.linea - 1].agregar(
                nodo_actual.linea, nodo_actual.componente
            )
            nodo_actual = nodo_actual.siguiente

        nodo_actual = pasos_producto.cabeza

        while (
            nodo_actual
            or verificar_ensamblando(maquina)
            or any(not lista.esta_vacia() for lista in pasos_pendientes)
        ):
            tiempo_total += 1
            acciones = ["No hacer nada"] * maquina.cantidad_lineas
            fila = matriz.agregar_fila()

            ensamblando = False

            for i in range(maquina.cantidad_lineas):
                linea = maquina.lineas.obtener(i)
                if linea.tiempo_ensamblaje_restante > 0:
                    linea.tiempo_ensamblaje_restante -= 1
                    if linea.tiempo_ensamblaje_restante == 0:
                        acciones[i] = f"Ensamblar componente {linea.posicion_brazo}"
                    else:
                        acciones[i] = f"Ensamblando C{linea.posicion_brazo}"
                    ensamblando = True

            if not ensamblando and nodo_actual:
                for i in range(maquina.cantidad_lineas):
                    linea = maquina.lineas.obtener(i)
                    if not pasos_pendientes[i].esta_vacia():
                        paso = pasos_pendientes[i].cabeza
                        if paso.componente != linea.posicion_brazo:
                            acciones[i] = mover_brazo(linea, paso)
                        else:
                            pasos_pendientes[i].desencolar()
                            acciones[i] = iniciar_ensamblaje(linea, paso, maquina)
                            ensamblando = True
                            nodo_actual = nodo_actual.siguiente
                            break  # Salir del bucle para que otras líneas no hagan nada

            for i, accion in enumerate(acciones):
                matriz.agregar_columna(fila, accion)

            print(
                f"{tiempo_total:6d} | "
                + " | ".join([f"{accion:28}" for accion in acciones])
            )

        print(
            f"\nEl producto {producto.nombre} se puede elaborar óptimamente en {tiempo_total} segundos."
        )
        return tiempo_total, matriz

    @staticmethod
    def _hay_lineas_trabajando(maquina):
        for i in range(maquina.cantidad_lineas):
            if maquina.lineas.obtener(i).tiempo_ensamblaje_restante > 0:
                return True
        return False
