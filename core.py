from env import load_env

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def load_spotify():
    env = load_env()

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = env["scope"], 
                                                client_id = env["client_id"], 
                                                client_secret = env["client_secret"], 
                                                redirect_uri = env["redirect_uri"]))
    
    return sp

def get_playlists(sp):
    raw_data = sp.current_user_playlists()
    
    data = []
    for p in raw_data["items"]:
        data.append([p["name"], p["images"][0]["url"], p["id"]])
    return data