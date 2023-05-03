from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib as jb
import spotipy
from os import getenv
import sqlite3

# creating the database and connecting to it.
DB = SQLAlchemy()


class Song(DB.Model):
    # step 1 put all songs in sqlite3

    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.Unicode(150))
    album = DB.Column(DB.Unicode(150))
    album_id = DB.Column(DB.Unicode(150))
    artists = DB.Column(DB.Unicode(150))
    artist_ids = DB.Column(DB.Unicode(150))
    track_number = DB.Column(DB.BigInteger, nullable=False)
    disc_number = DB.Column(DB.BigInteger, nullable=False)
    explicit = DB.Column(DB.BigInteger, nullable=False)
    danceability = DB.Column(DB.BigInteger, nullable=False)
    energy = DB.Column(DB.BigInteger, nullable=False)
    key = DB.Column(DB.BigInteger, nullable=False)
    loudness = DB.Column(DB.BigInteger, nullable=False)
    mode = DB.Column(DB.BigInteger, nullable=False)
    speechiness = DB.Column(DB.BigInteger, nullable=False)
    acousticness = DB.Column(DB.BigInteger, nullable=False)
    instrumentalness = DB.Column(DB.BigInteger, nullable=False)
    liveness = DB.Column(DB.BigInteger, nullable=False)
    valence = DB.Column(DB.BigInteger, nullable=False)
    tempo = DB.Column(DB.BigInteger, nullable=False)
    duration_ms = DB.Column(DB.BigInteger, nullable=False)
    time_signature = DB.Column(DB.BigInteger, nullable=False)
    year = DB.Column(DB.BigInteger, nullable=False)
    release_date = DB.Column(DB.BigInteger, nullable=False)

    def __repr__(self):
        return f'''<{self.id}, {self.name}, {self.album}, {self.album_id}, {self.artists}, {self.artist_ids},
       {self.track_number}, {self.disc_number}, {self.explicit}, {self.danceability}, {self.energy},
       {self.key}, {self.loudness}, {self.mode}, {self.speechiness}, {self.acousticness},
       {self.instrumentalness}, {self.liveness}, {self.valence}, {self.tempo}, {self.duration_ms},
       {self.time_signature}, {self.year}, {self.release_date}'''
    # be able to query sqlite
    # return nearest 5 neighbors


def TrainAndSave():
    dataframe = pd.read_csv('tracks_features.csv')
    df = dataframe.values
    df = pd.read_csv('tracks_features.csv')
    df = df.reset_index()

    # Drop old index to avoid confusing it for the new one
    df = df.drop(columns=['index'])

    df['explicit'] = df['explicit'].astype(int)

    usable_columns = ['explicit', 'danceability', 'energy', 'key', 'loudness',
                      'mode', 'liveness', 'valence', 'tempo', 'speechiness', 'acousticness', 'instrumentalness',
                      'time_signature', 'year']

    X = df[usable_columns]
    neigh = NearestNeighbors(n_neighbors=5, n_jobs=-1)
    neigh.fit(X)
    # Look at the song that we want to find recommendations for
    filename = 'Spotifymodel.sav'
    jb.dump(neigh, filename)


def get_song_DB(song_name):
    conn = sqlite3.connect('db.sqlite3')
    query = f'''SELECT explicit, danceability, energy, key, loudness, 
            mode, liveness, valence, tempo, speechiness, acousticness, instrumentalness, time_signature, year FROM song WHERE song.name="{song_name}"'''
    curs = conn.cursor()
    result = curs.execute(query)
    songlist = []
    for song in result:
        songlist.append(song)
    return songlist[0]


def get_song_from_index(id):
    conn = sqlite3.connect('db.sqlite3')
    query = f'''SELECT name, artists FROM song WHERE song.level_0="{id}" '''
    curs = conn.cursor()
    result = curs.execute(query).fetchall()
    return result