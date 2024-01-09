# Importamos las librerías necesarias
from flask import Flask, render_template, request, flash
import sqlite3
import random

# Creamos la instancia de la aplicación Flask
app = Flask(__name__)

# Configuramos una clave secreta para los mensajes flash
app.secret_key = "flask_app"

# Creamos la conexión con la base de datos SQLite
conn = sqlite3.connect("codes.db", check_same_thread=False)
# Creamos el cursor para ejecutar las consultas
cur = conn.cursor()
# Creamos la tabla codes si no existe
cur.execute("CREATE TABLE IF NOT EXISTS codes ( TEXT PRIMARY KEY )")


# Definimos la ruta que muestra la pantalla con todos los códigos generados
@app.route("/all")
def all():
    # Obtenemos todos los códigos de la base de datos
    cur.execute("SELECT * FROM codes")
    codes = cur.fetchall()
    # Renderizamos la plantilla all.html pasando la lista de códigos
    return render_template("all.html", codes=codes)

# Definimos la ruta que muestra la pantalla de verificación de código
@app.route("/", methods=["GET", "POST"])
def check():
    # Si el método es POST, significa que el usuario ha introducido un código
    if request.method == "POST":
        # Obtenemos el código de los cuatro inputs del formulario
        code = "-".join([request.form[f"input{i}"] for i in range(1, 5)])
        # Comprobamos si el código existe en la base de datos
        cur.execute("SELECT * FROM codes WHERE code = ?", (code,))
        result = cur.fetchone()
        # Si el resultado es None, significa que el código no existe
        if result is None:
            # Mostramos un mensaje flash de error
            flash("El código no existe", "error")
        else:
            # Mostramos un mensaje flash de éxito
            flash("El código existe", "success")
    code = "-".join([str(random.randint(0, 9999)).zfill(4) for _ in range(4)])
    # Insertamos el código en la base de datos
    cur.execute("INSERT INTO codes VALUES (?)", (code,))
    # Guardamos los cambios
    conn.commit()
    return render_template("index.html",code= code)

# Ejecutamos la aplicación si se ejecuta este fichero
if __name__ == "__main__":
    app.run(debug=True)