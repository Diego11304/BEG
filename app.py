from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

db_config = {
    "host": "bpngdi36dwtobigkpb9r-mysql.services.clever-cloud.com",
    "user": "u7a32dpxdefscix0",
    "password": "Gk0Mwirj7wHkaxOUjl41",
    "database": "bpngdi36dwtobigkpb9r",
    "port": 3306
}

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")

        if user == USERNAME and pw == PASSWORD:
            session['user'] = user
            return redirect(url_for('productos'))
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    if 'user' in session:
        return redirect(url_for('productos'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/productos')
@login_required
def productos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos.html", productos=productos)

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion', '')
    precio = request.form['precio']
    stock = request.form['stock']
    imagen_url = request.form.get('imagen_url', '')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, precio, stock, imagen_url)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, descripcion, precio, stock, imagen_url))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/eliminar/<int:id_producto>')
@login_required
def eliminar(id_producto):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/editar/<int:id_producto>', methods=['POST'])
@login_required
def editar(id_producto):
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion', '')
    precio = request.form['precio']
    stock = request.form['stock']
    imagen_url = request.form.get('imagen_url', '')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s, imagen_url=%s
        WHERE id_producto=%s
    """, (nombre, descripcion, precio, stock, imagen_url, id_producto))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

if __name__ == '__main__':
    app.run(debug=True)
