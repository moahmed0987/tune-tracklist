import secret_keys
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_keys.app_config_secret_key

# login_manager = LoginManager()
# login_manager.init_app(app)

# basedir = os.path.abspath(os.path.dirname(__file__))

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "blog.db")

# db = SQLAlchemy(app)

from spotify_site import routes
