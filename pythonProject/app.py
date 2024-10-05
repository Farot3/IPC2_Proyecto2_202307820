import re
from flask import Flask, render_template, request, redirect, url_for, flash
import xml.etree.ElementTree as ET
import modules.ListaMaquina1 as LM
import modules.ListaSimple as LS
import modules.ListaProducto1 as LP
import modules.Listalinea as LL
import modules.ColaInstrucciones as CI
import modules.Cola as C
import modules.matriz as M
from modules.ListaElaboracionNodos import ListaElaboracionNodos
from modules.NodoElaboraciónFormateada import ListaPasos
from modules.NodoRelacion import ListaRelaciones
from modules.NodoProductoMatriz import ListaProductoMatriz
from modules.NodoMaquin import ListaMaquinas
from modules.NodoReporte import ListaReportes
from modules.secuenciaNodoCola import ListaNodos
from modules.ListanodoGrafica import ListaComponentes
from modules.NodoGráfica import ListaGraficas
from modules.ListaNodoSecuencia import ListaNodosSecuencia
import graphviz
import os
import shutil

maquinas = LM.ListaMaquina()
listaM = LS.ListaSimple()
nueva_lista_elaboracion_global = ListaElaboracionNodos()
lista_productos = LP.ListaProductos()  # Definir lista_productos globalmente
lista_elaboracion = ListaElaboracionNodos()
lista_producto_matriz = ListaProductoMatriz()
lista_maquinas = ListaMaquinas()
lista_reportes = ListaReportes()
lista_graficas = ListaGraficas()
lista_relaciones = ListaRelaciones()


app = Flask(__name__)
app.secret_key = "tu_clave_secreta"


def limpiar_directorio_uploads():
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            file_path = uploads_dir + "/" + filename  # Concatenación manual
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Archivo eliminado: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Directorio eliminado: {file_path}")
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")


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
    graficas = list(lista_graficas.obtener_todas())
    return render_template("reportes.html", reportes=reportes, graficas=graficas)


@app.route("/exportar_html")
def exportar_XML():
    exportar_xml()
    return redirect(url_for("index"))


@app.route("/buscar", methods=["GET", "POST"])
def index():
    global maquinas
    if request.method == "POST":
        uploaded_files = request.files.getlist("file")

        for uploaded_file in uploaded_files:
            if uploaded_file.filename.endswith(".xml"):
                file_path = os.path.join("uploads", uploaded_file.filename)

                # Crear el directorio 'uploads' si no existe
                if not os.path.exists("uploads"):
                    os.makedirs("uploads")
                    print("Directorio 'uploads' creado.")

                # Verificar si el archivo ya existe
                if os.path.exists(file_path):
                    print(f"El archivo '{file_path}' ya existe.")
                    # Leer y analizar el nuevo archivo
                    nuevas_maquinas, error1 = leer_archivo_xml(
                        uploaded_file, ListaMaquinas()
                    )
                    if error1:
                        os.remove(file_path)
                        print(f"Archivo '{file_path}' eliminado debido a un error.")
                        continue
                    # Sumar las nuevas máquinas al archivo existente
                    maquinas = sumar_maquinas(maquinas, nuevas_maquinas)
                else:
                    # Guardar el archivo temporalmente
                    uploaded_file.save(file_path)
                    print(f"Archivo guardado en '{file_path}'.")
                    maquinas, error1 = leer_archivo_xml(file_path, maquinas)
                    if error1:
                        # Eliminar el archivo si hay un error
                        os.remove(file_path)
                        print(f"Archivo '{file_path}' eliminado debido a un error.")
                        continue

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
    productos_seleccionados = LP.ListaProductos()

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


@app.route("/seleccionar_producto/<nombre_producto>", methods=["GET", "POST"])
def seleccionar_producto(nombre_producto):
    global lista_relaciones  # Asegurarse de que estamos usando la variable global
    global lista_productos
    global lista_reportes  # Asegurarse de que estamos usando la variable global

    producto_seleccionado = None
    elaboracion_seleccionada = None
    mostrar_simulacion = False  # Variable para controlar la visualización

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
                mostrar_simulacion=mostrar_simulacion,
                error="Error: La elaboración contiene un componente con valor C0.",
            )
    else:
        print("Producto o elaboración no encontrados")
        pasos_elaboracion = None

    # Procesar el tiempo ingresado por el usuario
    grafica_html = None
    grafica = None
    download_link = None
    tiempo = None
    tiempo_total = None
    nodo_producto_matriz = lista_producto_matriz.obtener_por_nombre(nombre_producto)
    if nodo_producto_matriz:
        matriz = nodo_producto_matriz.matriz
        tabla_html, error, tiempo_total = generar_tabla_html(matriz)
        if error:
            return render_template(
                "producto.html",
                producto=producto_seleccionado,
                pasos_elaboracion=pasos_elaboracion,
                mostrar_simulacion=mostrar_simulacion,
                error=error,
            )
        if request.method == "POST":
            mostrar_simulacion = True  # Mostrar la simulación después de procesar
            lista_reportes.agregar(
                nodo_producto_matriz.producto.nombre, pasos_elaboracion, tabla_html
            )
    else:
        tabla_html = None

    return render_template(
        "producto.html",
        producto=producto_seleccionado,
        pasos_elaboracion=pasos_elaboracion,
        tabla_html=tabla_html,
        grafica_html=grafica_html,
        grafica=grafica,
        download_link=download_link,
        tiempo=tiempo,
        tiempo_total=tiempo_total,
        mostrar_simulacion=mostrar_simulacion,
        error=None,
    )


@app.route("/mostrar_grafica/<nombre_producto>", methods=["POST"])
def mostrar_grafica(nombre_producto):
    global lista_producto_matriz
    global lista_reportes

    tiempo = request.form.get("tiempo")
    if tiempo:
        tiempo = int(tiempo)
        nodo_producto_matriz = lista_producto_matriz.obtener_por_nombre(nombre_producto)
        if nodo_producto_matriz:
            matriz = nodo_producto_matriz.matriz
            grafica_html = generar_grafica_html(tiempo, matriz)
            grafica = generar_grafica(
                tiempo, matriz, nombre_producto
            )  # Corregir la llamada
            tabla_html, error, tiempo_total = generar_tabla_html(matriz)
            if error:
                return render_template(
                    "producto.html",
                    producto=nodo_producto_matriz.producto,
                    pasos_elaboracion=ListaPasos(),
                    tabla_html=tabla_html,
                    grafica_html=grafica_html,
                    grafica=grafica,
                    tiempo=tiempo,
                    tiempo_total=tiempo_total,
                    mostrar_simulacion=True,  # Asegurarse de que la simulación se muestre
                    error=error,
                )

            return render_template(
                "producto.html",
                producto=nodo_producto_matriz.producto,
                pasos_elaboracion=ListaPasos(),  # Mantener los pasos de elaboración
                tabla_html=tabla_html,
                grafica_html=grafica_html,
                grafica=grafica,
                tiempo=tiempo,
                tiempo_total=tiempo_total,
                mostrar_simulacion=True,  # Asegurarse de que la simulación se muestre
                error=None,
            )

    return redirect(url_for("seleccionar_producto", nombre_producto=nombre_producto))


def sumar_maquinas(maquinas_existentes, nuevas_maquinas):
    for i in range(nuevas_maquinas.tamano):
        nueva_maquina = nuevas_maquinas.obtener(i)
        maquinas_existentes.agregar(nueva_maquina)
    return maquinas_existentes


def generar_grafica(tiempo, matriz, nombre_producto):
    fila_actual = matriz.cabeza
    fila = 0

    # Recorrer hasta el segundo especificado
    for _ in range(tiempo):
        if fila_actual is None:
            break
        fila_actual = fila_actual.abajo
        fila += 1

    if fila_actual is None:
        return "<p>No hay datos para el segundo especificado.</p>", None

    # Crear un objeto Digraph de graphviz
    dot = graphviz.Digraph(
        comment="Secuencia de Instrucciones", graph_attr={"rankdir": "LR"}
    )

    columna_actual = fila_actual
    lista_componentes = ListaComponentes()

    # Obtener los datos de la primera columna
    if columna_actual is not None:
        valor = columna_actual.valor if columna_actual.valor is not None else ""
        if valor and valor != "0" and "No hacer nada" not in valor:
            for componente in valor.split(","):
                lista_componentes.agregar(componente)

    # Agregar nodos y aristas al gráfico
    componentes = lista_componentes.obtener_componentes()
    anterior = None
    for componente in componentes:
        dot.node(componente, componente)
        if anterior:
            dot.edge(anterior, componente)
        anterior = componente

    # Renderizar el gráfico a un archivo y devolver el HTML para incrustarlo
    output_path = "static/secuencia_instrucciones"
    dot.render(output_path, format="png", cleanup=True)
    grafica_html = f'<img src="/static/secuencia_instrucciones.png" alt="Secuencia de Instrucciones">'

    # Guardar la gráfica en la lista de gráficas
    lista_graficas.agregar(nombre_producto, grafica_html)

    return grafica_html


def generar_grafica_html(tiempo, matriz):
    fila_actual = matriz.cabeza
    fila = 0

    # Recorrer hasta el segundo especificado
    for _ in range(tiempo):
        if fila_actual is None:
            break
        fila_actual = fila_actual.abajo
        fila += 1

    if fila_actual is None:
        return "<p>No hay datos para el segundo especificado.</p>"

    grafica_html = "<ul>"
    columna_actual = fila_actual
    columna = 0

    # Solo tomar los datos de la primera columna
    if columna_actual is not None:
        valor = columna_actual.valor if columna_actual.valor is not None else ""
        if valor and valor != "0" and "No hacer nada" not in valor:
            grafica_html += f"<li>{valor}</li>"

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
        listaProductos = LS.ListaSimple()

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
    tiempo_total = 0

    while fila_actual is not None:
        tabla_html += "<tr>"
        columna_actual = fila_actual

        # Saltar la primera columna
        if columna_actual is not None:
            columna_actual = columna_actual.siguiente

        while columna_actual is not None:
            valor = columna_actual.valor if columna_actual.valor is not None else ""
            if valor == 0:
                error = True
            tabla_html += f"<td>{valor}</td>"
            columna_actual = columna_actual.siguiente

        tabla_html += "</tr>"
        fila_actual = fila_actual.abajo
        tiempo_total += 1  # Incrementar el tiempo total por cada fila

    tabla_html += "</table>"

    if error:
        return (
            None,
            "Error: No se puede generar la tabla porque hay un componente con valor 0, lo cual está fuera de la dimensión de la tabla.",
            None,
        )
    return (
        tabla_html,
        None,
        tiempo_total - 1,
    )


def leer_archivo_xml(archivo, maquinas):
    global nueva_lista_elaboracion_global  # Asegurarse de que estamos usando la variable global
    global lista_elaboracion
    global lista_productos
    global lista_relaciones
    global lista_maquinas
    error1 = False
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
            productos = LP.ListaProductos()
            lineas = LL.ListaLineas()
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
                producto = CI.ColaInstrucciones()
                nombreProducto = producto_xml.find("nombre").text.strip()
                producto.nombreProducto = nombreProducto.strip()

                instrucciones = producto_xml.find("elaboracion").text

                matches_lineas = re.findall(r"L(\d+)", instrucciones)
                max_ln = max(int(ln) for ln in matches_lineas) if matches_lineas else 0

                if int(cantidadLineas) < max_ln:
                    flash(
                        f"La cantidad de líneas es menor que las elaboraciones de ensamblajes de las líneas en el archivo: {archivo}"
                    )
                    error1 = True
                    continue

                matches = re.findall(r"L\d+C(\d+)", instrucciones)
                max_m = max(int(m) for m in matches) if matches else 0

                if int(cantidadComponentes) < max_m:
                    flash(
                        f"La cantidad de componentes es menor que las elaboraciones de ensamblajes de los componentes en el archivo: {archivo}"
                    )
                    error1 = True
                    return maquinas, error1
                print(f"hola carnal {cantidadComponentes}, {tiempoEnsamblaje}")

                # Agregar a la nueva lista de elaboraciones
                nueva_lista_elaboracion.agregar(nombreProducto, instrucciones)
                lista_elaboracion.agregar(
                    nombreProducto, instrucciones
                )  # Llenar lista_elaboracion

                listaSecuencia = LS.ListaSimple()

                for _ in range(int(cantidadLineas)):
                    secuenciaComponente = C.Cola()
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
            print(f"depurando la vida {cantidadComponentes}, {tiempoEnsamblaje}")
            maquinas.agregar(lineas, productos)
            print(f"más falso que mi vida {cantidadComponentes}, {tiempoEnsamblaje}")
            # Agregar nodo de máquina a la lista de máquinas
            print(
                f"Agregando máquina: {nombre}, {cantidadLineas}, {cantidadComponentes}, {tiempoEnsamblaje}"
            )
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
        print(
            f"El archivo '{archivo.filename}' no existe. Por favor, verifica el directorio."
        )
        error1 = True
    except ET.ParseError:
        print(f"El archivo '{archivo.filename}' no es un archivo XML válido.")
        error1 = True
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}", "error")
        error1 = True

    return maquinas, error1  # Devolver la lista de máquinas


def ejecutarInstrucciones(noMaquina, noProducto):
    global maquinas  # Asegurarse de que estamos usando la variable global
    maquina = maquinas.obtener(noMaquina)
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
    # Agregar una columna extra al principio de la matriz
    matrizDatos = M.Matriz(2, lineas.noLineas + 2, nombreProducto)
    matrizDatos.establecer_valor(0, 1, "Tiempo ")
    matrizDatos.establecer_valor(0, 0, "Secuencia ")

    for i in range(lineas.noLineas):
        matrizDatos.establecer_valor(0, i + 2, "Linea " + str(i + 1))
    n = 1

    # Lista para almacenar todas las secuencias activas
    secuencias_activas = ListaNodosSecuencia()

    # Inicializar todas las secuencias al principio
    for i in range(lineas.noLineas):
        secuencia = secuencias.obtener(i)
        while not secuencia.esta_vacia():
            componente = secuencia.primero()
            secuencias_activas.agregar(f"L{i+1}C{componente}")
            secuencia.desencolar()

    # Restaurar las secuencias originales
    for i in range(lineas.noLineas):
        secuencia = secuencias.obtener(i)

        for secuencia_activa in secuencias_activas.obtener_todos():
            if secuencia_activa.startswith(f"L{i+1}"):
                componente = int(secuencia_activa.split("C")[1])
                secuencia.encolar(componente)

    while productoEnsamblado:
        lineaEnsamblar = -1
        todas_vacias = True  # Asume que todas las secuencias están vacías
        secuencias_ejecutadas = ListaNodos()

        for i in range(lineas.noLineas):
            secuencia = secuencias.obtener(i)
            linea = lineas.obtener(i)

            if not secuencia.esta_vacia():
                todas_vacias = False  # Al menos una secuencia no está vacía
                componente = secuencia.primero()
                instruccion = instrucciones.primero()

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
                            i + 2,
                            "Ensamblar - componente " + str(instruccion.componente),
                        )
                        secuencias_ejecutadas.agregar(f"L{linea.id}C{componente}")
                    else:
                        matrizDatos.establecer_valor(n, i + 2, "No hacer nada")
                else:
                    if int(linea.pos) < componente:
                        linea.moverAdelante()
                        matrizDatos.establecer_valor(
                            n, i + 2, "Mover brazo - componente " + str(linea.pos)
                        )
                        secuencias_ejecutadas.agregar(f"L{linea.id}C{componente}")
                    elif int(linea.pos) > componente:
                        linea.moverAtras()
                        matrizDatos.establecer_valor(
                            n, i + 2, "Mover brazo - componente " + str(linea.pos - 1)
                        )
                        secuencias_ejecutadas.agregar(f"L{linea.id}C{componente}")
                    elif int(linea.pos) == componente:
                        matrizDatos.establecer_valor(n, i + 2, "No hacer nada")
            else:
                matrizDatos.establecer_valor(n, i + 2, "No hacer nada")

        # Almacenar la secuencia que se está evaluando en la columna extra
        matrizDatos.establecer_valor(n, 0, str(secuencias_activas))
        matrizDatos.establecer_valor(n, 1, "Segundo " + str(n))

        if lineaEnsamblar != -1:
            lineas.obtener(lineaEnsamblar).ensamblar()

        n += 1

        if lineaEnsamblar != -1 and lineas.obtener(lineaEnsamblar).ensamblado:
            lineas.obtener(lineaEnsamblar).ensamblado = False
            instrucciones.desencolar()
            secuencias.obtener(lineaEnsamblar).desencolar()
            secuencia_a_eliminar = f"L{lineaEnsamblar+1}C{instruccion.componente}"
            secuencias_activas.eliminar(secuencia_a_eliminar)
            lineaEnsamblar = -1

        if todas_vacias or instrucciones.primeroEnsamblado() is None:
            productoEnsamblado = False
            break
        else:
            matrizDatos.anadir_fila()

    productoEnsamblado = True
    return matrizDatos


def exportar_xml():
    global maquinas  # Asegurarse de que estamos usando la variable global

    root = ET.Element("SalidaSimulacion")

    maquina_actual = maquinas.cabeza
    while maquina_actual is not None:
        maquina_element = ET.SubElement(root, "Maquina")
        nombre_element = ET.SubElement(maquina_element, "Nombre")
        nombre_element.text = (
            maquina_actual.maquina.nombreMaquina
        )  # Corregir el acceso al nombre de la máquina

        listado_productos_element = ET.SubElement(maquina_element, "ListadoProductos")
        producto_actual = maquina_actual.productos.cabeza
        while producto_actual is not None:
            producto_element = ET.SubElement(listado_productos_element, "Producto")
            nombre_producto_element = ET.SubElement(producto_element, "Nombre")
            nombre_producto_element.text = (
                producto_actual.nombre
            )  # Corregir el acceso al nombre del producto

            # Generar la tabla HTML para el producto usando la matriz
            nodo_producto_matriz = lista_producto_matriz.obtener_por_nombre(
                producto_actual.nombre
            )
            if nodo_producto_matriz:
                matriz = nodo_producto_matriz.matriz
                tabla_html, error, tiempo_total = generar_tabla_html(matriz)
                if error:
                    print(
                        f"Error al generar la tabla HTML para el producto {producto_actual.nombre}: {error}"
                    )
                    producto_actual = producto_actual.siguiente
                    continue

                # Extraer la información de la tabla HTML y agregarla al XML
                tiempo_total_element = ET.SubElement(producto_element, "TiempoTotal")
                tiempo_total_element.text = str(tiempo_total)

                elaboracion_optima_element = ET.SubElement(
                    producto_element, "ElaboracionOptima"
                )
                fila_actual = matriz.cabeza.abajo  # Omitir la primera fila
                segundo = 1
                while fila_actual is not None:
                    tiempo_element = ET.SubElement(
                        elaboracion_optima_element, "Tiempo", NoSegundo=str(segundo)
                    )
                    columna_actual = fila_actual.siguiente  # Omitir la primera columna
                    if columna_actual is not None:
                        columna_actual = (
                            columna_actual.siguiente
                        )  # Omitir la segunda columna
                    no_linea = 1
                    while columna_actual is not None:
                        linea_element = ET.SubElement(
                            tiempo_element, "LineaEnsamblaje", NoLinea=str(no_linea)
                        )
                        linea_element.text = (
                            columna_actual.valor
                            if columna_actual.valor is not None
                            else "No hacer nada"
                        )
                        columna_actual = columna_actual.siguiente
                        no_linea += 1
                    fila_actual = fila_actual.abajo
                    segundo += 1

            producto_actual = producto_actual.siguiente

        maquina_actual = maquina_actual.siguiente

    tree = ET.ElementTree(root)
    tree.write("exportación.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    limpiar_directorio_uploads()
    app.run(debug=True)
