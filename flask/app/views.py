from typing import List, Dict
import mysql.connector
import json
import os
from flask import request, render_template, jsonify
from app import app


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    nombre_usuario = request.form['text1']
    word = request.args.get('text1')
    password_usuario = request.form['text2']

    mydb = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="catalogos"
    )
    mycursor = mydb.cursor()
    sql = "SELECT password_usuario FROM usuarios WHERE nombre_usuario = %s"
    user = (nombre_usuario, )
    mycursor.execute(sql, user)
    myresult = mycursor.fetchone()
    print(myresult[0])
    if myresult[0] == password_usuario:
        result = {
            "output": "SI ES ADMIN!!!"
        }
        print ("siessssss adminnnnn")
    else:
        result = {
            "output": "NO ES ADMIN!!!"
        }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)


@app.route('/db')
def index_db() -> str:
    return json.dumps({'favorite_colors': favorite_colors()})



@app.route('/usuarios')
def usuarios():
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
    data = (result)
    #data = (("1","Mariana","Mariana123"),("2","Fher","Fher123"))
    return render_template('usuarios.html',headings=headings,data=data)