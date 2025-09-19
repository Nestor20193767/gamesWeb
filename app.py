from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Carpeta con tus archivos
DATOS_FOLDER = os.path.join(app.root_path, 'datos')

@app.route('/datos/<path:filename>')
def serve_file(filename):
    # Devuelve el archivo tal cual, sin abrirlo
    return send_from_directory(DATOS_FOLDER, filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/a-todos-lados")
def a_todos_lados():
    return render_template("a_todos_lados.html")

@app.route("/dilo-sin-roche")
def Dilo_Sin_Roche():
    return render_template("dilo_sin_roche.html")

@app.route("/3-2-1-tomen")
def Tomen_3_2_1():
    return render_template("321tone.html")

@app.route("/timer")
def timer():
    return render_template("diccionario_prueba.html") # Puede variar el template para hacer las pruebas


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
