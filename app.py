import hashlib
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, session
from werkzeug.utils import secure_filename 

app = Flask(__name__) 
app.secret_key = "asdfghjkl123"
FOLDER_IMAGENES = "static/imagenes/"

@app.route("/", methods=["get"])
def index():
    return render_template("index.html") 

@app.route("/iniciar/", methods=["post"])
def login():
    usuario = request.form["usuario"]
    password = request.form["contraseña"]
    clave = hashlib.sha256(password.encode())
    pwd = clave.hexdigest()
    if not usuario or not password: 
        return "Se necesita usuario/contraseña. Porfavor regresar e ingresar los datos correctos"
    if len(usuario) > 15:
        return "Usuario excede longitud maxima. Porfavor regresar e ingresar los datos correctos"
    if len(password) > 20:
        return "Contraseña excede longitud maxima. Porfavor regresar e ingresar los datos correctos"

    with sqlite3.connect ("Base_Comentarios.db") as con:
        cur = con.cursor()
        cur.execute("SELECT 1 FROM Usuarios WHERE id = ? AND contraseña = ?", [usuario, pwd])
        if cur.fetchone():     
            session["usuario"]=usuario
            return redirect("/usuario/") 
    return redirect("/no_usuario/")

@app.route("/no_usuario/")
def no_usuario():
    return render_template("no_usuario.html")

@app.route("/registro/", methods=["post"])
def regristro():
    return render_template("registro.html")

@app.route("/registro/crear/", methods=["post"])
def registro_crear():
    user = request.form["reg_usuario"]
    password = request.form["reg_contraseña"]
    clave = hashlib.sha256(password.encode())
    pwd = clave.hexdigest()
    with sqlite3.connect("Base_Comentarios.db") as con: 
        cur = con.cursor()
        cur.execute("SELECT id FROM Usuarios WHERE id=?", [user])
        if cur.fetchone():
            return redirect("/existe_usuario/")
        cur.execute("INSERT INTO Usuarios (id,contraseña) VALUES (?,?);", [user, pwd])
        con.commit()
        return redirect("/usuario_creado/")

@app.route("/existe_usuario/")
def existe_usuario():
    return render_template("existe_usuario.html")

@app.route("/usuario_creado/")
def usuario_creado():
    return render_template("usuario_creado.html")

@app.route("/usuario/")
def usuario():
    return render_template("usuario.html", nombre = session["usuario"])

@app.route("/usuario/sub_imagen/", methods=["post"])
def sub_imagen():
    imagen = request.files["subir_imagen"]
    nom_archivo = imagen.filename
    ruta = FOLDER_IMAGENES + secure_filename(nom_archivo)
    imagen.save(ruta)
    with sqlite3.connect("Base_Comentarios.db") as con: 
        cur = con.cursor()
        cur.execute("INSERT INTO Imagenes (ruta,usuario) VALUES (?,?);", [ruta,session["usuario"]])
        con.commit()
    return redirect("/imagen_subida/")

@app.route("/imagen_subida/")
def imagen_subida():
    return render_template("imagen_subida.html", nombre = session["usuario"])

@app.route("/agr_comentario/")
def agr_comentario():
    return 

@app.route("/buscar/")
def buscar():
    return render_template("buscar.html", nombre = session["usuario"])

@app.route("/buscar/bus_usuario")
def bus_usuario():
    return 

@app.route("/mensajes/env_mensaje/")
def env_mensajes():
    return 

@app.route("/mensajes/")
def mensajes():
    return render_template("mensajes.html", nombre = session["usuario"])

@app.route("/logout/")
def logout():
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)