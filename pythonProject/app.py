import re
from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import modules.ListaMaquina1 as lm
import modules.ListaSimple as ls
import modules.ListaProducto1 as lp
import modules.Listalinea as ll
import modules.ColaInstrucciones as ci
import modules.Cola as c
import modules.matriz as m
from modules.ListaElaboracionNodos import ListaElaboracionNodos
from modules.NodoElaboraciónFormateada import ListaPasos
from modules.NodoRelacion import ListaRelaciones
from modules.NodoProductoMatriz import ListaProductoMatriz
from modules.NodoMaquin import ListaMaquinas
from modules.NodoReporte import ListaReportes

maquinas = lm.ListaMaquina()
listaM = ls.ListaSimple()
nueva_lista_elaboracion_global = ListaElaboracionNodos()
lista_productos = lp.ListaProductos()  # Definir lista_productos globalmente
lista_elaboracion = ListaElaboracionNodos()
lista_producto_matriz = ListaProductoMatriz()
lista_maquinas = ListaMaquinas()
lista_reportes = ListaReportes()


app = Flask(__name__)
app.secret_key = "tu_clave_secreta"


@app.route("/")
def Entrada():
    global maquinas  # Asegurarse de que estamos usando la variable global
    return render_template("index.html", Maquinas=maquinas)


@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")


@app.route("/reportes")
def reporte():
    global lista_reportes  # Asegurarse de que estamos usando la variable global
    reportes = list(lista_reportes)
    return render_template("reportes.html", reportes=reportes)


@app.route("/buscar", methods=["GET", "POST"])
def index():
    global maquinas  # Declarar que vamos a usar la variable global
    if request.method == "POST":
        uploaded_files = request.files.getlist("file")

        for uploaded_file in uploaded_files:
            if uploaded_file.filename.endswith(".xml"):
                maquinas = leer_archivo_xml(uploaded_file, maquinas)
                if maquinas.tamano > 0:
                    procesar_info(0)
            else:
                return "Solo se permiten archivos .xml", 400

        return render_template("index.html", Maquinas=maquinas)

    return render_template("index.html", Maquinas=maquinas)


@app.route("/seleccionar_maquina/<nombre_maquina>")
def seleccionar_maquina(nombre_maquina):
    global maquinas  # Asegurarse de que estamos usando la variable global
    # Buscar la máquina seleccionada
    maquina_seleccionada = maquinas.obtener_por_nombre(nombre_maquina)
    productos_seleccionados = lp.ListaProductos()

    if maquina_seleccionada:
        print(
            f"Máquina seleccionada: {maquina_seleccionada.maquina.get_nombre_maquina()}"
        )
        producto_actual = maquina_seleccionada.productos.cabeza
        while producto_actual:
            print(f"Agregando producto: {producto_actual.nombre}")
            productos_seleccionados.agregar(
                producto_actual.valor, producto_actual.nombre, producto_actual.valor2
            )
            producto_actual = producto_actual.siguiente

        # Obtener y mostrar los nombres de los productos
        nombres_productos = productos_seleccionados.obtener_nombres_productos()
        actual_nombre = nombres_productos.cabeza
        while actual_nombre is not None:
            print(f"Producto en lista: {actual_nombre.nombre}")
            actual_nombre = actual_nombre.siguiente

    return render_template(
        "index.html",
        Maquinas=maquinas,
        maquina_seleccionada=maquina_seleccionada,
        nombres_productos=nombres_productos,
    )


def _procesar_elaboracion(elaboracion):
    lista_pasos = ListaPasos()
    matches = re.findall(r"L\d+C\d+", elaboracion)
    error = False
    for match in matches:
        if "C0" in match:
            error = True
        lista_pasos.agregar(match)
    return lista_pasos, error


# Definir lista_relaciones globalmente
lista_relaciones = ListaRelaciones()


@app.route("/seleccionar_producto/<nombre_producto>", methods=["GET", "POST"])
def seleccionar_producto(nombre_producto):
    global lista_relaciones  # Asegurarse de que estamos usando la variable global
    global lista_productos
    global lista_reportes  # Asegurarse de que estamos usando la variable global

    producto_seleccionado = None
    elaboracion_seleccionada = None

    # Buscar la relación del producto seleccionado
    actual_relacion = lista_relaciones.cabeza
    while actual_relacion:
        if actual_relacion.nodo_producto.nombre == nombre_producto:
            producto_seleccionado = actual_relacion.nodo_producto
            elaboracion_seleccionada = actual_relacion.nodo_elaboracion
            break
        actual_relacion = actual_relacion.siguiente

    # Verificar si se encontró la relación
    if producto_seleccionado and elaboracion_seleccionada:
        pasos_elaboracion, error = _procesar_elaboracion(
            elaboracion_seleccionada.elaboracion
        )
        print(f"Producto seleccionado: {producto_seleccionado.nombre}")
        print(f"Elaboración seleccionada: {elaboracion_seleccionada.elaboracion}")
        if error:
            return render_template(
                "producto.html",
                producto=producto_seleccionado,
                pasos_elaboracion=pasos_elaboracion,
                error="Error: La elaboración contiene un componente con valor C0.",
            )
    else:
        print("Producto o elaboración no encontrados")
        pasos_elaboracion = None

    # Procesar el tiempo ingresado por el usuario
    grafica_html = None
    tiempo = None
    nodo_producto_matriz = lista_producto_matriz.obtener_por_nombre(nombre_producto)
    if nodo_producto_matriz:
        matriz = nodo_producto_matriz.matriz
        tabla_html, error = generar_tabla_html(matriz)
        if error:
            return render_template(
                "producto.html",
                producto=producto_seleccionado,
                pasos_elaboracion=pasos_elaboracion,
                error=error,
            )

        if request.method == "POST":
            tiempo = request.form.get("tiempo")
            if tiempo:
                tiempo = int(tiempo)
                grafica_html = generar_grafica_html(tiempo, matriz)
                lista_reportes.agregar(
                    producto_seleccionado.nombre, pasos_elaboracion, tabla_html
                )
    else:
        tabla_html = None

    return render_template(
        "producto.html",
        producto=producto_seleccionado,
        pasos_elaboracion=pasos_elaboracion,
        tabla_html=tabla_html,
        grafica_html=grafica_html,
        tiempo=tiempo,
        error=None,
    )


def generar_grafica_html(tiempo, matriz):
    fila_actual = matriz.cabeza
    for _ in range(tiempo):
        if fila_actual is None:
            break
        fila_actual = fila_actual.abajo

    if fila_actual is None:
        return "<p>No hay datos para el segundo especificado.</p>"

    grafica_html = "<ul>"
    columna_actual = fila_actual
    while columna_actual is not None:
        valor = columna_actual.valor if columna_actual.valor is not None else ""
        if valor and valor != "0":  # Filtrar los que no hacen nada
            grafica_html += f"<li>{valor}</li>"
        columna_actual = columna_actual.siguiente
    grafica_html += "</ul>"
    return grafica_html


def generar_div_componentes(componentes):
    div_html = "<div>"
    for componente in componentes:
        div_html += f"<p>{componente}</p>"
    div_html += "</div>"
    return div_html


def procesar_info(n):
    global maquinas  # Asegurarse de que estamos usando la variable global
    for i in range(maquinas.tamano - n):
        listaProductos = ls.ListaSimple()

        for j in range(maquinas.obtener_por_indice(i + n).productos.tamano):
            matrizProcesada = ejecutarInstrucciones(i + n, j)
            matrizProcesada.imprimirDatos()
            matrizProcesada.imprimir_matriz()
            listaProductos.agregar(matrizProcesada)
            listaProductos.cabeza.nombre = (
                maquinas.obtener_por_indice(i + n).productos.obtener(j).nombre
            )
            # Agregar a la lista de productos y matrices
            producto = maquinas.obtener_por_indice(i + n).productos.obtener(j)
            lista_producto_matriz.agregar(producto, matrizProcesada)
        listaM.agregar(listaProductos)


def generar_tabla_html(matriz):
    fila_actual = matriz.cabeza
    tabla_html = "<table border='1'>"
    error = False

    while fila_actual is not None:
        tabla_html += "<tr>"
        columna_actual = fila_actual

        while columna_actual is not None:
            valor = columna_actual.valor if columna_actual.valor is not None else ""
            if valor == 0:
                error = True
            tabla_html += f"<td>{valor}</td>"
            columna_actual = columna_actual.siguiente

        tabla_html += "</tr>"
        fila_actual = fila_actual.abajo

    tabla_html += "</table>"

    if error:
        return (
            None,
            "Error: No se puede generar la tabla porque hay un componente con valor 0, lo cual está fuera de la dimensión de la tabla.",
        )
    return tabla_html, None


def leer_archivo_xml(archivo, maquinas):
    global nueva_lista_elaboracion_global  # Asegurarse de que estamos usando la variable global
    global lista_elaboracion
    global lista_productos
    global lista_relaciones
    global lista_maquinas
    try:
        tree = ET.parse(archivo)
        root = tree.getroot()

        if root.tag != "ListaMaquinas":
            print(
                "Error: El archivo XML debe comenzar con la etiqueta <ListaMaquinas>."
            )
            return maquinas

        nueva_lista_elaboracion = ListaElaboracionNodos()

        for maquinas_xml in root.findall("Maquina"):
            productos = lp.ListaProductos()
            lineas = ll.ListaLineas()
            nombre = maquinas_xml.find("NombreMaquina").text.strip()
            lineas.set_nombre_maquina(nombre)

            cantidadLineas = maquinas_xml.find("CantidadLineasProduccion").text.strip()
            cantidadComponentes = maquinas_xml.find("CantidadComponentes").text.strip()
            tiempoEnsamblaje = maquinas_xml.find("TiempoEnsamblaje").text.strip()

            lineas.noLineas = int(cantidadLineas)
            lineas.tiempoEnsamblaje = int(tiempoEnsamblaje)
            for _ in range(int(cantidadLineas)):
                lineas.agregar(int(cantidadComponentes), int(tiempoEnsamblaje))

            listaProductos = maquinas_xml.find("ListadoProductos")

            for producto_xml in listaProductos.findall("Producto"):
                producto = ci.ColaInstrucciones()
                nombreProducto = producto_xml.find("nombre").text.strip()
                producto.nombreProducto = nombreProducto.strip()

                instrucciones = producto_xml.find("elaboracion").text

                # Agregar a la nueva lista de elaboraciones
                nueva_lista_elaboracion.agregar(nombreProducto, instrucciones)
                lista_elaboracion.agregar(
                    nombreProducto, instrucciones
                )  # Llenar lista_elaboracion

                listaSecuencia = ls.ListaSimple()

                for _ in range(int(cantidadLineas)):
                    secuenciaComponente = c.Cola()
                    listaSecuencia.agregar(secuenciaComponente)

                # Usar split para eliminar espacios extras y dividir las instrucciones
                partes = instrucciones.split()

                producto.noInstrucciones = len(partes)

                for parte in partes:
                    if parte.startswith("L"):
                        # Extraer la parte de la línea después de 'L' hasta encontrar 'C'
                        indice_C = parte.find("C")
                        if indice_C != -1:
                            linea = parte[1:indice_C]
                            componente = parte[indice_C + 1 :]

                            # Verificar que tanto línea como componente sean números válidos
                            if linea.isdigit() and componente.isdigit():
                                producto.encolar(int(linea), int(componente))
                                listaSecuencia.obtener(int(linea) - 1).encolar(
                                    int(componente)
                                )

                                # print(f"Línea: {linea}, Componente: {componente}")
                            else:
                                print(
                                    f"Error: Línea o componente no válidos en la instrucción '{parte}'"
                                )
                        else:
                            print(
                                f"Error: No se encontró 'C' en la instrucción '{parte}'"
                            )

                productos.agregar(producto, nombreProducto, listaSecuencia)
                lista_productos.agregar(
                    producto, nombreProducto, listaSecuencia
                )  # Llenar lista_productos
            # productos.mostrar()

            maquinas.agregar(lineas, productos)

            # Agregar nodo de máquina a la lista de máquinas
            lista_maquinas.agregar(
                nombre,
                int(cantidadLineas),
                int(cantidadComponentes),
                int(tiempoEnsamblaje),
            )

        nueva_lista_elaboracion.mostrar()

        # Relacionar las listas de productos y elaboraciones
        lista_relaciones = ListaRelaciones()

        nodo_producto = lista_productos.cabeza
        nodo_elaboracion = lista_elaboracion.cabeza

        while nodo_producto is not None and nodo_elaboracion is not None:
            if nodo_producto.nombre == nodo_elaboracion.nombre:
                lista_relaciones.agregar(nodo_producto, nodo_elaboracion)
                print(
                    f"Relacionando producto: {nodo_producto.nombre} con elaboración: {nodo_elaboracion.elaboracion}"
                )
                nodo_producto = nodo_producto.siguiente
                nodo_elaboracion = nodo_elaboracion.siguiente
            else:
                nodo_producto = nodo_producto.siguiente

    except FileNotFoundError:
        print(f"El archivo '{archivo}' no existe. Por favor, verifica el directorio.")
    except ET.ParseError:
        print(f"El archivo '{archivo}' no es un archivo XML válido.")
    except Exception as e:
        print(f"Error: {e}")

    return maquinas  # Devolver la lista de máquinas


def ejecutarInstrucciones(noMaquina, noProducto):
    global maquinas  # Asegurarse de que estamos usando la variable global
    maquina = maquinas.obtener_por_indice(noMaquina)
    nombreMaquina = maquina.productos.nombreMaquina
    producto = maquina.productos.obtener(noProducto)
    instrucciones = producto.valor
    secuencias = producto.valor2
    pasosExtra = maquina.maquina.tiempoEnsamblaje
    pasosExtra2 = maquina.maquina.tiempoEnsamblaje

    lineas = maquina.maquina

    for i in range(lineas.noLineas):
        lineas.obtener(i).ensamblado = False
        lineas.obtener(i).pos = 0

    nombreProducto = instrucciones.nombreProducto
    productoEnsamblado = True
    matrizDatos = m.Matriz(2, lineas.noLineas + 1, nombreProducto)
    matrizDatos.establecer_valor(0, 0, "Segundo ")

    for i in range(lineas.noLineas):
        matrizDatos.establecer_valor(0, i + 1, "Linea " + str(i + 1))
    n = 1

    while productoEnsamblado:
        lineaEnsamblar = -1
        instruccion = instrucciones.primero()
        todas_vacias = True  # Asume que todas las secuencias están vacías

        for i in range(lineas.noLineas):
            secuencia = secuencias.obtener(
                i
            )  # Asegúrate de obtener la secuencia correcta aquí
            linea = lineas.obtener(i)

            if not secuencia.esta_vacia():
                todas_vacias = False  # Al menos una secuencia no está vacía
                componente = secuencia.primero()

                if (
                    instruccion.linea == linea.id
                    and linea.pos == instruccion.componente
                ):
                    if not lineas.obtener(i).ensamblado:
                        pasosExtra -= 1
                        if pasosExtra == 0:
                            lineaEnsamblar = i
                            pasosExtra = pasosExtra2
                        matrizDatos.establecer_valor(
                            n,
                            i + 1,
                            "Ensamblar - comoponente " + str(instruccion.componente),
                        )

                    else:
                        matrizDatos.establecer_valor(n, i + 1, "No hacer nada")
                else:
                    if int(linea.pos) < componente:
                        linea.moverAdelante()
                        matrizDatos.establecer_valor(
                            n, i + 1, "Mover brazo - componente " + str(linea.pos)
                        )
                    elif int(linea.pos) > componente:
                        linea.moverAtras()
                        matrizDatos.establecer_valor(
                            n, i + 1, "Mover brazo - componente " + str(linea.pos)
                        )
                    elif int(linea.pos) == componente:
                        matrizDatos.establecer_valor(n, i + 1, "No hacer nada")
            else:
                matrizDatos.establecer_valor(n, i + 1, "No hacer nada")
        matrizDatos.establecer_valor(n, 0, "Segundo" + str(n))

        if lineaEnsamblar != -1:
            lineas.obtener(lineaEnsamblar).ensamblar()
            # print("Linea: ", lineaEnsamblar, "ensamblada")

        n += 1

        if lineaEnsamblar != -1 and lineas.obtener(lineaEnsamblar).ensamblado:
            lineas.obtener(lineaEnsamblar).ensamblado = False
            instrucciones.desencolar()
            secuencias.obtener(
                lineaEnsamblar
            ).desencolar()  # Desencola correctamente de la secuencia actual
            lineaEnsamblar = -1  # Resetear líneaEnsamblar para evitar el bucle infinito

        # Verificar si ya no hay más instrucciones que ensamblar
        if todas_vacias or instrucciones.primeroEnsamblado() is None:
            productoEnsamblado = False
            break
        else:
            matrizDatos.anadir_fila()
    # matrizDatos.imprimirDatos()
    # matrizDatos.imprimir_matriz()
    productoEnsamblado = True
    return matrizDatos


if __name__ == "__main__":
    app.run(debug=True)
