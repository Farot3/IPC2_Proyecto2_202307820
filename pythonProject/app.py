from flask import Flask, render_template, request, session
from modules.ListaMaquina import leer_maquina

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"


@app.route("/")
def Entrada():
    print("Antes de render_template")
    return render_template("index.html")


@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")


@app.route("/buscar", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["file"]

        if uploaded_file.filename.endswith(".xml"):
            # Leer el archivo XML y procesarlo
            contenido_archivo = uploaded_file.read().decode(
                "utf-8"
            )  # Decodificar a UTF-8
            lista_maquinas = leer_maquina(
                contenido_archivo
            )  # Pasar el contenido a la función leer_maquina
            print("La máquina se ha leído")
            lista_maquinas.imprimir()
            return render_template("index.html", maquinas=lista_maquinas)
        else:
            return "Solo se permiten archivos .xml", 400

    return render_template("index.html")


@app.route("/seleccionar", methods=["POST"])
def seleccionar_maquina():
    maquina_seleccionada = request.form.get("maquina")
    lista_maquinas = session.get("lista_maquinas")

    productos = None
    if lista_maquinas and maquina_seleccionada:
        maquina = lista_maquinas.buscar_maquina(maquina_seleccionada)
        if maquina:
            productos = []
            producto_actual = maquina.productos
            while producto_actual:
                productos.append(producto_actual)
                producto_actual = producto_actual.siguiente

    return render_template(
        "index.html",
        maquinas=lista_maquinas,
        maquina_seleccionada=maquina_seleccionada,
        productos=productos,
    )


@app.route("/seleccionar_producto", methods=["POST"])
def seleccionar_producto():
    producto_seleccionado = request.form.get("producto")
    return f"Producto seleccionado: {producto_seleccionado}"


if __name__ == "__main__":
    app.run(debug=True)
