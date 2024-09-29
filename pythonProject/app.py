from flask import Flask, render_template, request
from modules.ListaMaquina import leer_maquina, ListaMaquina
from modules.NodoProductoSeleccionado import NodoProductoSeleccionado
from modules.ListaProductoSeleccionado import ListaProductoSeleccionado
from modules.Esamblaje import Simulador

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"

lista_maquinas_global = ListaMaquina()


@app.route("/")
def Entrada():
    return render_template("index.html", maquinas=lista_maquinas_global)


@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")


@app.route("/buscar", methods=["GET", "POST"])
def index():
    global lista_maquinas_global
    if request.method == "POST":
        uploaded_files = request.files.getlist("file")

        for uploaded_file in uploaded_files:
            if uploaded_file.filename.endswith(".xml"):
                contenido_archivo = uploaded_file.read().decode("utf-8")
                lista_maquinas_global = leer_maquina(
                    contenido_archivo, lista_maquinas_global
                )
            else:
                return "Solo se permiten archivos .xml", 400

        lista_maquinas_global.imprimir()
        return render_template("index.html", maquinas=lista_maquinas_global)

    return render_template("index.html", maquinas=lista_maquinas_global)


@app.route("/seleccionar_maquina/<nombre_maquina>")
def seleccionar_maquina(nombre_maquina):
    global lista_maquinas_global

    # Buscar la máquina seleccionada
    maquina_seleccionada = lista_maquinas_global.buscar_maquina(nombre_maquina)
    productos_seleccionados = ListaProductoSeleccionado()
    if maquina_seleccionada:
        producto_actual = maquina_seleccionada.productos.cabeza
        while producto_actual:
            nodo_producto_seleccionado = NodoProductoSeleccionado(producto_actual)
            productos_seleccionados.agregar(nodo_producto_seleccionado)
            producto_actual = producto_actual.siguiente

    return render_template(
        "index.html",
        maquinas=lista_maquinas_global,
        maquina_seleccionada=maquina_seleccionada,
        productos=productos_seleccionados,
    )


@app.route("/seleccionar_producto/<nombre_producto>", methods=["GET", "POST"])
def seleccionar_producto(nombre_producto):
    global lista_maquinas_global

    maquina_seleccionada = None
    producto_seleccionado = None

    # Buscar el producto seleccionado y la máquina correspondiente
    actual_maquina = lista_maquinas_global.cabeza
    while actual_maquina:
        producto_actual = actual_maquina.productos.cabeza
        while producto_actual:
            if producto_actual.nombre == nombre_producto:
                maquina_seleccionada = actual_maquina
                producto_seleccionado = producto_actual
                break
            producto_actual = producto_actual.siguiente
        if producto_seleccionado:
            break
        actual_maquina = actual_maquina.siguiente

    return render_template(
        "producto.html",
        maquina=maquina_seleccionada,
        producto=producto_seleccionado,
    )


@app.route("/producto/<nombre_maquina>/<nombre_producto>", methods=["GET", "POST"])
def producto(nombre_maquina, nombre_producto):
    maquina = lista_maquinas_global.buscar_maquina(nombre_maquina)
    if not maquina:
        return "Máquina no encontrada", 404

    nodo_producto = maquina.productos.buscar_producto(nombre_producto)
    if not nodo_producto:
        return "Producto no encontrado", 404

    producto = nodo_producto  # Usar directamente el nodo_producto

    resultado_simulacion = None
    if request.method == "POST":
        print("Solicitud POST recibida")  # Mensaje de depuración
        tiempo_total, resultado_simulacion = Simulador.simular(
            maquina, producto
        )  # Cambiar a simular
        # Imprimir el resultado en consola
        print(
            f"El producto {producto.nombre} se puede elaborar óptimamente en {tiempo_total} segundos."
        )
        nodo_actual = resultado_simulacion.pasos.cabeza
        while nodo_actual:
            nodo_actual = nodo_actual.siguiente

    return render_template(
        "producto.html",
        maquina=maquina,
        producto=producto,
        resultado_simulacion=resultado_simulacion,
    )


if __name__ == "__main__":
    app.run(debug=True)
