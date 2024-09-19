from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def Entrada():
    return render_template("index.html")


@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")


if __name__ == "__main__":
    app.run(debug=True)
