import json
import logging
import random

import spotipy
from flask import Flask
from flask_apscheduler import APScheduler
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
scheduler = APScheduler()


@scheduler.task('cron', id='generate', day_of_week='*', hour=0, minute=0)
def generate():
    class Track:
        def __init__(self, genre_track, song_track):
            self.genre_track = genre_track
            self.song_track = song_track

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    with open('genres.txt') as file:
        genres_list = [line.rstrip() for line in file]

    tracks_list = []
    genres_list = random.sample(genres_list, 10)
    app.logger.info('Genres: \n' + ', '.join(genres_list))

    for genre in random.sample(genres_list, 10):
        total = sp.search(genre, limit=1)['tracks']['total']
        offset = random.randint(0, total)
        items = sp.search('genre:' + genre, limit=10, offset=offset)['tracks']['items']
        if len(items) > 0:
            i = 0
            while items[i]['preview_url'] is None and i < len(items):
                i += 1
            song = items[i]['preview_url']
            tracks_list.append(Track(genre, song))
    f = open("generated.json", "w")
    f.write(json.dumps([ob.__dict__ for ob in tracks_list], indent=len(tracks_list)))
    f.close()
    return "Sucesso", 200, {"Access-Control-Allow-Origin": "*"}


@app.route('/random-daily-songs/get', methods=['GET'])
def get():
    with open('generated.json', 'r') as handle:
        return json.load(handle)


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.logger.setLevel(logging.INFO)
    app.run(host="44.226.145.213")