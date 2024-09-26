from app import app, db
from flask import redirect, render_template, url_for
from app.forms import RegistrationForm, LoginForm
from flask_login import current_user, login_user
from app.models import User 


@app.route("/")
@app.route("/index")#esto se llama endpoint, url  o vista. Y la mayoria de endopoints nos llevaran a un html o links a otras vistas
#La idea es que simpre devuelva algo, para que el usuario pueda ir navegando por la página web.
def index():#Este método es obligatorio y corresponde con el home o la página principal.
    return render_template("index.html", title= "Home")

@app.route("/login", methods= ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return render_template("index.html", title= "Home")
    form= LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return render_template("index.html", title="Home")
            else: 
                error= "Contraseña incorrecta"
                return render_template("login.html", form=form, error=error)
        else:
            return redirect(url_for("register"))
    return render_template("login.html", form=form, error="")


@app.route("/register", methods=["GET", "POST"])#Una web, para el intercambio de paquetes o de info, usa el protocolo HTTP, y este trabaja mediante 4 metodos principales:GET(mostrar algo), POST(recoger algo: info... mediante fromularios por ejemplo), PUT, DELETE
def register():
    # TODO: comprobar si el usuario se ha autenticado
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form= RegistrationForm()
    if form.validate_on_submit():#Esta funcion ejecutará todas las validaciones que hayamos hecho en el formulario cuando nosotros hagamos un post.
        #TODO: en caso de que el registro se haga correctamente, debo crearle la cuenta al usuario y guardarlo en la db.
        user= User(username=form.username.data, mail= form.email.data)
        user.set_password(password= form.password.data)
        db.session.add(user)#guardamos el usuario que acabamos de registrar correctamente en la db
        db.session.commit()#esto sirve para ejecutar o llevar a acabo el add previo.
        return render_template("index.html", title= "Home")
    return render_template("register.html", form=form)#De lo contrario, vuelvo a mostrarle la página de registro para que lo vuelva a intentar.
