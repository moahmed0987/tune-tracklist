from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "884011ca4843c9a29b388da5b6bf229824c3f0fc55f2ea79"

# login_manager = LoginManager()
# login_manager.init_app(app)

# basedir = os.path.abspath(os.path.dirname(__file__))

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "blog.db")

# db = SQLAlchemy(app)

from spotify_site import routes