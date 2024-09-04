from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy #me permite crear bases de datos usando solo python, ya que te evita tener que usar un lenguaje de base de datos
from flask_migrate import Migrate#este se encarga de la gestion de las migraciones(modificaciones) que le vaya haciendo a la base de datos, eliminar, agregar, modifcar cosas...

app = Flask(__name__,static_url_path= "/static")
app.config.from_object(Config)
#estas dos configuraciones extras son simplmente a modo eficiencia. Los he puesto aqui pero podrían ir perfectamente en el fichero de config.py
#La primera sirve para que solo salgan 10 recetas por pagina, de lo contrario se tendrian que cargar todas las recetas de golpe y tardaría mucho
#Y la segunda es para que muestre solo dos mensajes por pagina
app.config["RECIPES_PER_PAGE"]= 10 
app.config["MESSAGES_PER_PAGE"]=2

db = SQLAlchemy(app)
migrate = Migrate(app, db)
