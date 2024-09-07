import os
from flask.cli import load_dotenv

basedir= os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")#esto es muy importante, es información reservada, que no se va a ver cuando publiquemos la página, pero será necesaria ternela para implementar los formularios.LA INFO SE VA A ENCRIPTAR EN BASE A ESTA PALABRA

    SQLACHEMY_DATABE_URI = os.environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://") or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICACION= False