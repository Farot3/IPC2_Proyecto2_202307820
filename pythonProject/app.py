from flask import Flask, render_template, request
from modules.ListaMaquina import leer_maquina, ListaMaquina
from modules.NodoProductoSeleccionado import NodoProductoSeleccionado
from modules.ListaProductoSeleccionado import ListaProductoSeleccionado

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
        uploaded_file = request.files["file"]

        if uploaded_file.filename.endswith(".xml"):
            contenido_archivo = uploaded_file.read().decode("utf-8")
            lista_maquinas_global = leer_maquina(contenido_archivo)
            lista_maquinas_global.imprimir()

            return render_template("index.html", maquinas=lista_maquinas_global)
        else:
            return "Solo se permiten archivos .xml", 400

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


@app.route("/seleccionar_producto/<nombre_producto>")
def seleccionar_producto(nombre_producto):
    producto_seleccionado = nombre_producto
    return f"Producto seleccionado: {producto_seleccionado}"


if __name__ == "__main__":
    app.run(debug=True)
