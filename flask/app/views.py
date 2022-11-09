from typing import List, Dict
from flask_mysqldb import MySQL
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import mysql.connector
import json
import os
import base64
from flask import request, render_template, jsonify, Response, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, FileField, SelectField, PasswordField, validators)
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo
from werkzeug.utils import secure_filename
from app import app
import time
import glob
from werkzeug.datastructures import MultiDict


app.config['SECRET_KEY']="admin123"
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'catalogos'
db = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

class User(UserMixin):

    def __init__(self, id, username, password, first_name, second_name, user_type) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.second_name = second_name
        self.user_type = user_type

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

class ModelUser():
    @classmethod
    def login(self, db, username):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_user, username, password, first_name, second_name, user_type FROM users WHERE username = '{}'""".format(username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], row[2], row[3], row[4], row[5])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_user, username, first_name, second_name, user_type FROM users WHERE id_user = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3], row[4])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        


@login_manager.user_loader
def load_user(id_user):
    return ModelUser.get_by_id(db, id_user)

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

    cursor.execute(sql, ("Catalogo Ejemplo","Descripcion ejemplo",archivo_binario,"archivo_ejemplo.pdf","admin",))
    conn.commit()

#agregar_catalogo_ejemplo()

class CatalogoForm(FlaskForm):
    #time.sleep(180)
    nombre = StringField('Nombre catalogo', validators=[InputRequired(),Length(min=10, max=100)])
    descripcion = TextAreaField('Descripcion catalogo',validators=[InputRequired(),Length(max=200)])
    archivo = FileField('Archivo catalogo')


class UsuarioForm(FlaskForm):
    #time.sleep(180)
    usuario = StringField('Usuario', [validators.Length(min=3, max=25)])
    nombre = StringField('Nombre', [validators.Length(min=2, max=35)])
    apellido = StringField('Apellido', [validators.Length(min=2, max=35)])
    tipo = SelectField(u'Tipo Usuario', choices=[('1', 'Admin'), ('2', 'Normal')])
    password = PasswordField("Contraseña:", validators=[DataRequired(), Length(min=5)], id="password")
    confirmar = PasswordField("Confirmar Contraseña:", validators=[DataRequired(), EqualTo('password', message="Las contraseñas no son iguales")], id="conpassword")
 
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('catalogos')) 
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
    user = ModelUser.login(db,nombre_usuario)
    print("SIIU")
    print(user.password)
    print(password_usuario)
    print(user.username)
    if(user):
        if(user.password == password_usuario):
            login_user(user)
            return redirect(url_for('catalogos'))    
    return redirect(url_for('home'))


@app.route('/agregar_catalogo', methods=['POST','GET'])
@login_required
def agregar_catalogo():
    form = CatalogoForm()
    if request.method == 'POST':
        if form.is_submitted():
            nombre_catalogo = form.nombre.data
            descripcion_catalogo = form.descripcion.data
            file = request.files['file']
            archivo_binario = file.read()
            archivo_nombre = secure_filename(file.filename)
            conn = conexion_db()
            sql = "INSERT INTO catalogs (catalog_name,catalog_description,file,filename,id_user) VALUES (%s,%s,%s,%s,%s)"
            cursor = conn.cursor()
            cursor.execute(sql, (nombre_catalogo,descripcion_catalogo,archivo_binario,archivo_nombre,current_user.id,))
            conn.commit()
            print("se guardo!!!!")
            return redirect(url_for('catalogos'))     
    return render_template('agregar_catalogo.html', form=form)

@app.route('/agregar_usuario', methods=['POST','GET'])
@login_required
def agregar_usuario():
    form = UsuarioForm()
    if request.method == 'POST':
        if form.is_submitted():
            usuario = form.usuario.data
            nombre = form.nombre.data
            apellido = form.apellido.data
            password = form.password.data
            tipo_usuario = form.tipo.data
            print("----------------------- **************************")
            print(tipo_usuario)
            conn = conexion_db()
            sql = "INSERT INTO users (username,first_name,second_name,password,user_type) VALUES (%s,%s,%s,%s,%s)"
            cursor = conn.cursor()
            cursor.execute(sql, (usuario,nombre,apellido,password,tipo_usuario,))
            conn.commit()
            print("se guardo!!!!")
            return redirect(url_for('usuarios'))     
    return render_template('agregar_usuario.html', form=form)

@app.route('/getFile', methods=['GET'])
def getFile():
    try:
        select_catalogo = "SELECT file, filename FROM catalogs WHERE id_catalog = {}".format(request.args.get('id'))
        conn = conexion_db()
        cursor = conn.cursor()
        cursor.execute(select_catalogo)
        myresult = cursor.fetchone()
        print(myresult[1])
        filename,extension = os.path.splitext(myresult[1])
        print(extension)
        print(filename)
        print("SIUs")
        return Response(myresult[0], mimetype="text/"+extension, headers={"Content-disposition": "attachment; filename="+filename+"."+extension})
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error)) 
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
            print("MySQL connection is closed")
    return None

@app.route('/dynamic_panel', methods=['GET'])
def dynamic_panel():
    return render_template('dynamic_panel.html')


@app.route('/dynamic_panel_2', methods=['GET'])
def dynamic_panel_2():
    return render_template('dynamic_panel_2.html')

@app.route('/get_panels', methods=['GET'])
def get_panels():
    files_folder = "./app/static/files/"
    x = request.args.getlist('x[]')
    y = request.args.getlist('y[]')
    import pathlib
    total_files = []
    for x_label in x:
        x_path = files_folder+x_label+"/"
        print(x_path)
        
        if(len(y) == 0): 
            total_files = total_files + sorted( filter( os.path.isfile, glob.glob(x_path + '*') ) )
        
        else: 
            for y_label in y:
                y_path = x_path + y_label+"/"
                print(y_path)
                total_files = total_files + sorted( filter( os.path.isfile, glob.glob(y_path + '*') ) )
    total_files = [file.split("./app")[1] for file in total_files]
    print(total_files)
            
    result = {"total_files":len(total_files), "paths":total_files}
    


    return (result,200)
    

@app.route('/catalogos')
@login_required
def catalogos():
    conn = conexion_db()
    select_usuarios = "SELECT id_catalog,catalog_name,catalog_description FROM catalogs where id_user = {}".format(current_user.id)
    cursor = conn.cursor()
    cursor.execute(select_usuarios)
    result = cursor.fetchall()
    data = []
    data0 = []
    for i in range (len(result)):
        for j in range(3):
            data0.append(result[i][j]) 
            
        data.append(data0)
        data0 = []
        print("HOLA13bbbb23")
    return render_template('catalogos.html',data=data)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/usuarios')
@login_required
def usuarios():
    if(current_user.user_type == 1):
        cursor = db.connection.cursor()
        sql = "SELECT id_user, username, first_name, second_name FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template('usuarios.html',data=result)
    
    return ('', 204)

#@app.route('/agregar_usuario', methods=['POST','GET'])
#@login_required
#def agregar_usuario():
#    form = UsuarioForm(request.form)
#    if request.method == 'POST' and form.validate():
#        user = User(form.usuario.data, form.nombre.data, form.apellido.data,
#                    form.password.data)
        #db_session.add(user)
#        flash('Thanks for registering')
#        return redirect(url_for('usuarios'))
#    return render_template('agregar_usuario.html', form=form)

@app.route('/actualizar_usuario', methods=['GET'])
@login_required
def actualizar_usuario():
    print(request.args.get('id'))
    result = None
    return render_template('actualizar_usuario.html',data=result)

@app.route('/actualizar_catalogo', methods=['GET','POST'])
@login_required
def get_catalogo():
    print("SIUU")
    print("SIUU")
    print("SIUU")
    
    form = CatalogoForm()
    id_catalog = request.args.get('id')
    print(id_catalog)
    if(request.method =='GET'):
        select_catalogo = "SELECT id_catalog, catalog_name, catalog_description FROM catalogs WHERE id_catalog = {}".format(id_catalog)
        conn = conexion_db()
        cursor = conn.cursor()
        cursor.execute(select_catalogo)
        result = cursor.fetchone()
        print(result)
        form.nombre.data = result[1]
        form.descripcion.data = result[2]
    if form.validate_on_submit():
        nombre_catalogo = form.nombre.data
        print("JAJAJA")
        print(nombre_catalogo)
        descripcion_catalogo = form.descripcion.data
        file = request.files['file']
        conn = conexion_db()
        cursor = conn.cursor()        
        if file.filename !='':
            file = request.files['file']
            archivo_binario = file.read()
            archivo_nombre = secure_filename(file.filename)
            sql = "UPDATE catalogs SET catalog_name = %s, catalog_description = %s, file = %s, filename = %s where id_catalog = %s"
            cursor.execute(sql, (nombre_catalogo,descripcion_catalogo, archivo_binario, archivo_nombre, id_catalog,))
            conn.commit()
        else:
            try:
                sql = "UPDATE catalogs SET catalog_name = %s, catalog_description = %s where id_catalog = %s"
                cursor.execute(sql, (nombre_catalogo,descripcion_catalogo,id_catalog,))
                conn.commit()
            except mysql.connector.Error as error:
                print("Failed to read BLOB data from MySQL table {}".format(error))
        return redirect(url_for('catalogos'))
    return render_template('actualizar_catalogo.html',form=form)
    

        