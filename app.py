from flask import Flask, render_template, request

app = Flask(__name__)
if __name__ == '__main__':
    app.run()

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/index/registro/")
def regristro():
    return render_template("registro.html")

@app.route("/index/usuario/")
def usuario():
    return render_template("usuario.html")

@app.route("/index/admin/")
def admin():
    return render_template("admin.html")

@app.route("/index/super_admin/")
def super_admin():
    return render_template("super_admin.html")

@app.route("/index/buscar/")
def buscar():
    return render_template("buscar.html")

@app.route("/index/mensajes/")
def mensajes():
    return render_template("mensajes.html")

@app.route("/index/super_admin/admin_admin/")
def admin_admin():
    return render_template("admin_admin.html")

@app.route("/index/admin/admin_usuario/")
def admin_usuario():
    return render_template("admin_usuario.html")