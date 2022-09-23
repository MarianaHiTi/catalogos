from flask import request, render_template, jsonify
import mysql.connector

conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="catalogos"
    )


select_usuarios = "SELECT * FROM usuarios"
cursor = conn.cursor()
cursor.execute(select_usuarios)
result = cursor.fetchall()

headings = ("ID Usuario", "Usuario", "Password")
#data = (result)
data = (("1","Mariana","Mariana123"),("2","Fher","Fher123"))

@app.route('/usuarios')
def home():
    return render_template('usuarios.html',headings=headings,data=data)