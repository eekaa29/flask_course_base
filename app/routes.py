from app import app, db
from flask import render_template

@app.route("/")
@app.route("/index")#esto se llama endpoint, url  o vista. Y la mayoria de endopoints nos llevaran a un html o links a otras vistas
#La idea es que simpre devuelva algo, para que el usuario pueda ir navegando por la página web.
def index():#Este método es obligatorio y corresponde con el home o la página principal.
    return render_template("index.html", title= "Home")