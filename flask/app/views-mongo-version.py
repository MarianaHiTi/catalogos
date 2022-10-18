from typing import List, Dict
import mysql.connector
import json
import os
import base64
from flask import request, render_template, jsonify, Response
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, FileField, SelectField)
from wtforms.validators import InputRequired, Length
from werkzeug.utils import secure_filename
from app import app
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


app.config['SECRET_KEY']="admin123"
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root-crashell', 
                         password='password-crashell',
                        authSource="admin")
    db = client["db_crashell"]
    return db"""
def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["catalogos_db"]
    return db

@app.route('/catalogos')
def get_stored_catalogos():
    db = get_db()
    _catalogos = db.catalogo_tb.find()
    catalogos = [{"id": catalogo["id"], "name": catalogo["name"], "description": catalogo["description"], "user": catalogo["user"]} for catalogo in _catalogos]
    return jsonify({"catalogos": catalogos})


"""@app.route('/api')
def get_api():
    data = {
        "server":   "cs_mongodb",
        "port":     '27017',
        "username": "root-crashell",
        "password": "password-crashell",
        "db":       "db_crashell"
    }

    response = ConnectionMongoDB(data).getDB()
    return Response(response=json.dumps(response), status=200, mimetype='application/json')"""

"""class CatalogoForm(FlaskForm):
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="catalogos"
    )
    select_usuarios = "SELECT nombre_usuario FROM usuarios"
    cursor = conn.cursor()
    cursor.execute(select_usuarios)
    result = list(cursor.fetchall())
    usuarios = [ item for elem in result for item in elem]
    nombre = StringField('Nombre catalogo', validators=[InputRequired(),
                                             Length(min=10, max=100)])
    descripcion = TextAreaField('Descripcion catalogo',
                                validators=[InputRequired(),
                                            Length(max=200)])
    archivo = FileField('Archivo catalogo')
    usuario = SelectField(u'Usuario catalogo', choices=usuarios)"""
 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/adminlte')
def admin():
    return render_template('adminlte.html')
    

"""@app.route('/join', methods=['GET','POST'])
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

    headings = ("wwww", "Usuario", "Password")
    data = (result)
    #data = (("1","Mariana","Mariana123"),("2","Fher","Fher123"))
    return render_template('usuarios.html',headings=headings,data=data)

@app.route('/agregar_catalogo', methods=('GET', 'POST'))
def adminblob():
    form = CatalogoForm()
    if request.method == 'POST':
        if form.is_submitted():
            nombre_catalogo = form.nombre.data
            descripcion_catalogo = form.descripcion.data
            usuario_catalogo = form.usuario.data
            file = request.files['file']
            archivo_binario = file.stream.read()
            archivo_nombre = secure_filename(file.filename)
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password="root",
                database="catalogos"
            )
            sql = "INSERT INTO catalogos (nombre_catalogo,descripcion_catalogo,archivo_catalogo,archivo_nombre,usuario_catalogo) VALUES (%s,%s,%s,%s,%s)"
            cursor = conn.cursor()
            cursor.execute(sql, (nombre_catalogo,descripcion_catalogo,archivo_binario,archivo_nombre,usuario_catalogo,))
            conn.commit()
            print("se guardo")
           
    return render_template('agregar_catalogo.html', form=form)

@app.route('/catalogos')
def catalogos():
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="catalogos"
    )

    select_usuarios = "SELECT id_catalogo,nombre_catalogo,descripcion_catalogo,usuario_catalogo FROM catalogos"
    cursor = conn.cursor()
    cursor.execute(select_usuarios)
    result = cursor.fetchall()
    data = []
    data0 = []
    for i in range (len(result)):
        for j in range(6):
            if(j == 4):
                data0.append("BLOB")
            else:
                if(j == 5):
                    data0.append("button")
                else:    
                    data0.append(result[i][j]) 
            
        data.append(data0)
        data0 = []
    
    print(data)


    return render_template('catalogos.html',data=data)"""