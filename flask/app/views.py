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


app.config['SECRET_KEY']="admin123"
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def conexion_db():
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="catalogos"
    )
    return conn

##### AGREGAR CATALOGO EN AUTOMATICO PARA EJEMPLO
def agregar_catalogo_ejemplo():
    conn = conexion_db()
    sql = "INSERT INTO catalogos (nombre_catalogo,descripcion_catalogo,archivo_catalogo,archivo_nombre,usuario_catalogo) VALUES (%s,%s,%s,%s,%s)"
    cursor = conn.cursor()
    with open("app/CV_MarianaHinojosa.pdf","rb") as pdf_file:
        archivo_binario = pdf_file.read()

    cursor.execute(sql, ("Catalogo Ejemplo","Descripcion ejemplo",archivo_binario,"archivo_ejemplo","Mariana Hinojosa",))
    conn.commit()

#agregar_catalogo_ejemplo()

class CatalogoForm(FlaskForm):
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
    usuario = SelectField(u'Usuario catalogo', choices=usuarios)
 
@app.route('/')
def home():
    return render_template('home.html')
    

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/adminlte')
def admin():
    return render_template('adminlte.html')
    
@app.route('/join', methods=['POST'])
def my_form_post():
    nombre_usuario = request.form['text1']
    #word = request.args.get('text1')
    password_usuario = request.form['text2']
    conn = conexion_db()
    mycursor = conn.cursor()
    sql = "SELECT password_usuario FROM usuarios WHERE nombre_usuario = %s"
    user = (nombre_usuario, )
    mycursor.execute(sql, user)
    myresult = mycursor.fetchone()
    if myresult[0] == password_usuario:
        print ("siessssss adminnnnn --------------")
        print("1234e8283930039383838")
        return catalogos()
    else:
        print("NO ES ADMIN")
        return home()

@app.route('/usuarios')
def usuarios():
    conn = conexion_db
    select_usuarios = "SELECT * FROM usuarios"
    cursor = conn.cursor()
    cursor.execute(select_usuarios)
    result = cursor.fetchall()
    headings = ("wwww", "Usuario", "Password")
    data = (result)
    #data = (("1","Mariana","Mariana123"),("2","Fher","Fher123"))
    return render_template('usuarios.html',headings=headings,data=data)

@app.route('/agregar_catalogo', methods=['POST','GET'])
def agregar_catalogo():
    form = CatalogoForm()
    if request.method == 'POST':
        if form.is_submitted():
            nombre_catalogo = form.nombre.data
            descripcion_catalogo = form.descripcion.data
            usuario_catalogo = form.usuario.data
            file = request.files['file']
            archivo_binario = file.read()
            archivo_nombre = secure_filename(file.filename)
            conn = conexion_db()
            sql = "INSERT INTO catalogos (nombre_catalogo,descripcion_catalogo,archivo_catalogo,archivo_nombre,usuario_catalogo) VALUES (%s,%s,%s,%s,%s)"
            cursor = conn.cursor()
            cursor.execute(sql, (nombre_catalogo,descripcion_catalogo,archivo_binario,archivo_nombre,usuario_catalogo,))
            conn.commit()
            print("se guardo")
            return catalogos()
           
    return render_template('agregar_catalogo.html', form=form)

@app.route('/getFile', methods=['GET'])
def getFile():
    try:
        select_catalogo = "SELECT archivo_catalogo FROM catalogos WHERE id_catalogo = %s"
        id_catalogo = (request.args.get('id'),)
        conn = conexion_db()
        cursor = conn.cursor()
        cursor.execute(select_catalogo, id_catalogo)
        myresult = cursor.fetchone()
        return Response(myresult[0], mimetype="text/pdf", headers={"Content-disposition": "attachment; filename=1.pdf"})
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error)) 
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
            print("MySQL connection is closed")

@app.route('/catalogos')
def catalogos():
    conn = conexion_db()
    select_usuarios = "SELECT id_catalogo,nombre_catalogo,descripcion_catalogo,usuario_catalogo FROM catalogos"
    cursor = conn.cursor()
    cursor.execute(select_usuarios)
    result = cursor.fetchall()
    data = []
    data0 = []
    for i in range (len(result)):
        for j in range(4):
            data0.append(result[i][j]) 
            
        data.append(data0)
        data0 = []
    return render_template('catalogos.html',data=data)