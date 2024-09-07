from app import db


class CocktailDB(db.Model):#Entre paréntesis he puesto eso ya que queremos que la clase herede de "db.Model", la cualha sido creadaen el framework SQL-Alchemy,representa una tabla de nuentra base de datos. De esta manera me aseguro de que el SQL Alchemy entienda que la clase CocktailDB es una tabla de mi base de datos. Gracias a la herencia, evita tener que copiar y pegar todo el rato el código implementado en db.Model
    id = db.Column(db.Integer, primary_key=True)#La primary_key es un atributo que identifica a los elementos de esa tabla, asi es como se traslada lo que he explicado en el draw.io sobre el tema del id único para cada cocktel
    #Si yo inserto un cocktail con id 1, no puede haber otro diferente con el mismo id, para eso le establezco que la primary_key es el id
    name = db.Columnn(db.String(64), index= True, unique=True)#Lo de index es para que a la hora de buscar los nombres de los cockteles, esten ordenados, así será mas facil encontralos. Y unique para que no haya dos nombres iguales.No son obligatorios.
    ingredients = db.Column(db.Text(), nullable= False)#Aqui le digo que va a ser un Texto porque va a ser un campo de texto grande. Por eso no le pongo string
    preparation = db.Column(db.Text(), nullable= False)#Lo de nullable es para que no pueda ser nulo.


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