import os
import uuid

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask

load_dotenv()

_iteration = 5

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/save_recent_spotify_tracks')
def save_recent_spotify_tracks():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                       client_secret=SPOTIPY_CLIENT_SECRET,
                                                       redirect_uri=SPOTIPY_REDIRECT_URI,
                                                       scope="user-read-recently-played playlist-modify-public playlist-modify-private"))
        recent_tracks = list()

        _tracks = sp.current_user_recently_played()
        # recent_tracks.append(_tracks['items'])

        # for i in range(_iteration):
        #     _tracks = sp.current_user_recently_played(limit=50, after=i*50)
        #     recent_tracks.append(_tracks['items'])

        playlist_id = sp.user_playlist_create(
            sp.current_user()['id'], f'auto_recent_{uuid.uuid4().hex}')['id']
        track_ids = [x['track']['id'] for x in _tracks['items']]

        snapshot = sp.playlist_add_items(playlist_id, track_ids)

        response = 'Tracks saved successfully'
    except Exception as e:
        response = f'ERROR: {e}'
    finally:
        return response
