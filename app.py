from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    "host": "bpngdi36dwtobigkpb9r-mysql.services.clever-cloud.com",
    "user": "u7a32dpxdefscix0",
    "password": "Gk0Mwirj7wHkaxOUjl41",
    "database": "bpngdi36dwtobigkpb9r",
    "port": 3306
}

@app.route('/')
def index():
    return redirect(url_for('productos'))

@app.route('/productos')
def productos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos.html", productos=productos)

@app.route('/agregar', methods=['POST'])
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

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    stock = request.form['stock']
    imagen_url = request.form['imagen_url']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s, imagen_url=%s
        WHERE id=%s
    """, (nombre, descripcion, precio, stock, imagen_url, id))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

if __name__ == '__main__':
    app.run(debug=True)
