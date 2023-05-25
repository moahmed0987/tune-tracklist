
import time

import secret_keys
import spotipy
from flask import Flask, redirect, render_template, request, send_file, session, url_for
from spotipy.oauth2 import SpotifyOAuth
from time_periods import time_periods
import pandas as pd
import plotly.express as px
import plotly

from spotify_site import app


@app.route("/")
def home():
    return render_template("home.html", title="Home")

@app.route("/login/")
def login():
    oauth = create_oauth()
    auth_url = oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect/")
def handle_redirect():
    if session.get("next", False):
        next_url = session["next"]
        session.pop("next")

    oauth = create_oauth()
    session.clear()
    code = request.args.get("code")
    session["token_data"] = oauth.get_access_token(code)

    if next_url:
        return redirect(next_url)
    
    return redirect(url_for("home"))

@app.route("/artists/<time_period>/")
def top_artists(time_period): 
    if time_period not in time_periods: 
        return "Time period not found", 400
    
    token_data = get_token_data()
    if not token_data:
        print("User is not logged in")
        session["next"] = url_for("top_artists", time_period=time_period)
        return redirect(url_for("login"))
    
    spotify_api_client = spotipy.Spotify(auth=token_data["access_token"])
    top_artists = spotify_api_client.current_user_top_artists(limit=50, offset=0, time_range=time_period)["items"]

    return render_template("top_artists.html", title="Top Artists", top_artists=top_artists) 

@app.route("/artists/")
def top_artists_default():
    return redirect(url_for("top_artists", time_period="long_term"))

@app.route("/tracks/<time_period>/")
def top_tracks(time_period):
    if time_period not in time_periods: 
        return "Time period not found", 400

    token_data = get_token_data()
    if not token_data:
        print("User is not logged in")
        session["next"] = url_for("top_tracks", time_period=time_period)
        return redirect(url_for("login"))
    
    spotify_api_client = spotipy.Spotify(auth=token_data["access_token"])
    top_tracks = spotify_api_client.current_user_top_tracks(limit=50, offset=0, time_range=time_period)["items"]

    return render_template("top_tracks.html", title="Top Tracks", top_tracks=top_tracks) 

@app.route("/tracks/")
def top_tracks_default():
    return redirect(url_for("top_tracks", time_period="long_term"))

@app.route("/graphs")
def graphs():
    token_data = get_token_data()
    if not token_data:
        print("User is not logged in")
        return redirect(url_for("login"))
    spotify_api_client = spotipy.Spotify(auth=token_data["access_token"])

    top_artists = spotify_api_client.current_user_top_artists(limit=50, offset=0, time_range="long_term")["items"]
    genres = {}
    for track in top_artists:
        for genre in track['genres']:
            if genre in genres:
                genres[genre] += 1
            else:
                genres[genre] = 1
    data = [genres, {"label1":1, "label2":2, "label3":3}]
    
    df = pd.DataFrame({
        'genre': [_ for _ in data[0]],
        'value': [data[0][genre] for genre in data[0]]
    })
    fig = px.pie(df, values="value", names="genre")
    fig.update_traces(hoverinfo='label+percent', textposition='inside', textinfo='percent+label')
    fig.update_layout(title_text="Top Genres")
    graph_data = [plotly.io.to_html(fig=fig)]
    return render_template("graph.html", title="Graphs", graph_data=graph_data)
    
@app.route("/recent")
def recent():
    token_data = get_token_data()
    if not token_data:
        print("User is not logged in")
        session["next"] = url_for("recent")
        return redirect(url_for("login"))
    spotify_api_client = spotipy.Spotify(auth=token_data["access_token"])

    recent_tracks = spotify_api_client.current_user_recently_played(limit=50, after=None, before=None)["items"]

    return render_template("recent.html", title="Recent Tracks", recent_tracks=recent_tracks)

def create_oauth():
    return SpotifyOAuth(
        client_id=secret_keys.client_id,
        client_secret=secret_keys.client_secret,
        redirect_uri=url_for("handle_redirect", _external=True),
        scope="user-top-read user-read-recently-played"
    )

def get_token_data(): # returns token data if already logged in, otherwise False - should be handled and redirected to url_for("login")
    token_data = session.get("token_data", False)
    if not token_data:
        return False
    now = time.time()
    is_expired = token_data["expires_at"] - now < 60
    if is_expired:
        oauth = create_oauth()
        token_data = oauth.refresh_access_token(token_data["refresh_token"])
    return token_data

@app.route("/clearsession")
def clearsession():
    session.clear()
    session['token_data'] = None
    return redirect(url_for("home"))
