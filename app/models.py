from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class CocktailDB(db.Model):#Entre paréntesis he puesto eso ya que queremos que la clase herede de "db.Model", la cualha sido creada en el 
    #framework SQL-Alchemy,representa una tabla de nuentra base de datos. De esta manera me aseguro de que el SQL Alchemy entienda 
    #que la clase CocktailDB es una tabla de mi base de datos. Gracias a la herencia, evita tener que copiar y pegar todo el rato el código implementado en db.Model
    id = db.Column(db.Integer, primary_key=True)#La primary_key es un atributo que identifica a los elementos de esa tabla, 
    #asi es como se traslada lo que he explicado en el draw.io sobre el tema del id único para cada cocktel
    #Si yo inserto un cocktail con id 1, no puede haber otro diferente con el mismo id, para eso le establezco que la primary_key es el id
    name = db.Column(db.String(64), index= True, unique=True)#Lo de index es para que a la hora de buscar los nombres de los cockteles, esten ordenados, 
    #así será mas facil encontralos. Y unique para que no haya dos nombres iguales.No son obligatorios.
    ingredients = db.Column(db.Text(), nullable= False)#Aqui le digo que va a ser un Texto porque va a ser un campo de texto grande. Por eso no le pongo string
    preparation = db.Column(db.Text(), nullable= False)#Lo de nullable es para que no pueda ser nulo.

class Message(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    render_id= db.Column(db.Integer, db.ForeignKey("user.id"))#En estos dos casos le estoy diciendo que el valor hace referencia a camposo de otra tabla
    recipient_id= db.Column(db.Integer, db.ForeignKey("user.id"))#Son campos de otra tabla, y aquí establezco la conexión(de derecha a izquierda)representada en el mapa de flujo
    body= db.Column(db.String(140))
    timestamp= db.Column(db.DateTime, index= True, default=datetime.utcnow)
    def __repr__(self):
        return f"<Message {self.body}>"#Cada clase puede tener métodos asociados, en este caso el nombre del metodo es una palabra reservada.
    #Es un método muy común que sirve para representar el objeto(la clase).Cuando yo haga un print, python se va a preguntar: ¿Se ha definido
    # la funcion representation?, y al ver que si en vez de printarme únicamente el nombre del objeto y el id, me printará lo que yo haya confi-
    #gurado en el metodo __repr__
    # Cuando estamos representando objetos complejos, es decir, cosas que no son ni sets, ni datos simples, ni listas... Python no sabe muy 
    #bien cómo representarlas, es decir, si tu le dices imprímeme un cócktel, no sabrá cuál de todos los atributos imprimir(ingredients,
    # preparation...), y simplemente imprimiría el nombre de la clase y el id. Si quiero cambiar ese comportamiento, tendré que crear la clase
    #__repr__ para establecer en forma de string el formato que quiero que sigua la clase.(Usando self tengo acceso a cialquier atributo de la clase)

class User(UserMixin,db.Model):
    id= db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(64),index= True, unique= True)
    email = db.Column(db.String(120),index= True, unique= True)
    password_hash=db.Column(db.String(120))
    last_message_read_time= db.Column(db.DateTime)


    #Ahora voy a realizar la conexion representada en el mapa de flujo de las clases, esta vez de izquierda a derecha. Con lo que deberé repre-
    #sentar una lista, ya que el asterisco(usado en el mapa de flujo)significa un conjunto de datos. Dberé representar un conjunto de datos de 
    #los mensajes recibidos y de los enviados
    messages_sent= db.relationship("Message", foreign_keys= "Message.sender_id",
                                  backref= "author", lazy= "dynamic")#Para hacer refencia a un conjunto de datos se usa db.reationship, para un único elemento, se usa db.foreign_key.
    #usuario= message.recipient
    messages_received= db.relationship("Message", foreign_keys= "Message.recipient_id",
                                      backref="recipient", lazy="dynamic")#El orden a seguir es: Tabla o clase a la que hacemos referencia,
    #fila de la tabal a la que estamos referenciando, backref es como un manera de averiguar el emisor o receptor del mensaje, "buscar hacia atrás"
    #o ir de derecha a izquierda en las tablas, y por último lazy determinará cuando cargar la información en memoria, al poner dynamic no se 
    #cargarán hasta que el usuario acceda a este campo.



    #El hash sería como aplicarle a la contraseña un método llamado sha256 el cual coge la contrasña
    #y le aplica una encriptación,un string bastante largo el cual contiene la información de la contraseña normal pero encriptada.
    # se hace a modo de seguridad, para no tener que guardar la contraseña en la base de datos, ya que en caso de que nos entren en la base de
    # datos sería una negligencia tener las contraseñas de los usuarios ahí.
    def set_password(self, password):#Crear el hash de la contraseña con una función ya implementa de python, solo hay que importarla
        self.password_hash= generate_password_hash(password)
    
    def check_password(self, password):#Comprobar el hash de la contraseña con una función ya implementa de python, solo hay que importarla
        return check_password_hash(self.password_hash, password)

@login.user_loader#esto jutno con crear el objeto login manager en el fichero init, es lo que hay que hacer para autenficar el usuario(algo necesario en el fichero routes)
def load_user(id):
    return User.query.get(int(id))


'''Estos son los pasos a seguir para poner en funcionanto la base de datos:

1- Poner por la terminal el comando: set FLASK_APP=barkeeper.py
    Básicamente para deicr al progrmaa que lo primero que va a tener que ejecutar va a ser el fichero barkeeper.py. La profe dice que 
    es conveniente que si estamos trabajando en más de un proyecto a la vez, lo hagamos muy a menudo para asegurnarnos de que el programa
    sepa que este es el fichero raiz(el primero que se debe ejecutar).
2- Ingresar el comando: flask db init
    Sirve para inicializar la base de datos. SOLO HAY QUE HACERLO UNA VEZ, una vez inicializado no hace falta volver a ponerlo.
    Al poner el comando se nos creará el directorio "migrations" 
3- El siguiente paso es poner el comando: flask db migrate -m "comentario sobre la modificación". En este caso como el cambio que vamos a hacer 
    va a ser añadir la clase CocktailDB el comando podría ser: flask db migrate -m "Nueva clase Cocktail" 
    Este comado sirve para hacer una migración, decirle: oye, lee este fichero, generame un cambio nuevo y eso me lo guardas en la base de datos.
4- Bien, hasta este punto tengo los cambios guardados en la carpeta migrations, pero ahora el ultimo paso sería aplicar estos cambios a la base
     de datos. Así que para aplicar los cambios usaremos el comando: flask db upgrade.
    De esta manera le estamos diciendo, oye en base a mis migraciones(modificaciones) actualizame la base de datos.

EN EL CASO DE HABER COMETIDO UN ERROR NOS LO DIRÁ AL INGRESAR EL COMANDO flask db migrate -m ....
COMBIENE HACER ESTE PROCESO MUY AMENUDO YA QUE ASÍ EN CASO DE COMENTER ALGUN FALLO SABREMOS DONDE HA SIDO. SI EJECUTAMOS ESTE PROCESO CADA 100 
CAMBIOS VA A SER DIFICILÍSIMO SABER CUAL DE TODOS LOS CAMBIOS FUE EL QUE DIO PROBLEMAS.
RECUERDO QUE EL PASO DOS SOLO HAY QUE EJECUTARLO UNA VEZ, PORQUE LA BASE DE DATOS SOLO ES NECESARIO INICIALIZARLA LA PRIMERA VEZ QUE LA VAYAMOS
A USAR. LOS DOS COMANDOS SIGUIENTES COMBIENE HACERLO MUY A MENUDO.


'''