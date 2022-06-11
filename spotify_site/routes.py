from spotify_site import app
from flask import Flask, render_template, url_for
import secret_keys
from spotipy.oauth2 import SpotifyOAuth

@app.route("/home")
def home():
    return render_template('home.html', title="home")

