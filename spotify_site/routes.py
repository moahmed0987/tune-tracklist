import time

import secret_keys
import spotipy
from flask import Flask, redirect, render_template, request, session, url_for
from spotipy.oauth2 import SpotifyOAuth

from spotify_site import app

@app.route("/home")
def home():
    return render_template("home.html", title="Spotify Top Artists and Tracks")

@app.route("/login")
def login():
    oauth = create_oauth()
    auth_url = oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def handle_redirect():
    oauth = create_oauth()
    code = request.args.get("code")
    session["token_data"] = oauth.get_access_token(code)
    return redirect(url_for("home"))

@app.route("/showtopartists")
def top_artists():
    try:
        token_data = get_token_data()
    except ValueError:
        print("User is not logged in")
        return redirect(url_for("login"))
    spotify_api_client = spotipy.Spotify(auth=token_data["access_token"])
    top_artists = spotify_api_client.current_user_top_artists(limit=50, offset=0, time_range="long_term")["items"]

    return render_template("top_artists.html", title="Top Artists", top_artists=top_artists) 

@app.route("/showtoptracks")
def top_tracks():
    try:
        token_data = get_token_data()
    except ValueError:
        print("User is not logged in")
        return redirect(url_for("login"))
    spotify_api_client = spotipy.Spotify(auth=token_data["access_token"])
    top_tracks = spotify_api_client.current_user_top_tracks(limit=50, offset=0, time_range="long_term")["items"]
    return render_template("top_tracks.html", title="Top Tracks", top_tracks=top_tracks) 


def create_oauth():
    return SpotifyOAuth(
        client_id=secret_keys.client_id,
        client_secret=secret_keys.client_secret,
        redirect_uri=url_for("handle_redirect", _external=True),
        scope="user-top-read"
    )

def get_token_data():
    token_data = session.get("token_data", None)
    if token_data is None:
        raise ValueError("Token data is None")
    now = time.time()
    is_expired = token_data["expires_at"] - now < 60
    if is_expired:
        oauth = create_oauth()
        token_data = oauth.refresh_access_token(token_data["refresh_token"])
    return token_data
