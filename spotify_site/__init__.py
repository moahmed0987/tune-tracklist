import secret_keys
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_keys.app_config_secret_key

from spotify_site import routes
