from flask import Flask, render_template, request
from .models import DB, get_song_DB
from os import getenv
from .models import Song, get_song_DB, get_song_from_index
import joblib as jb
import numpy as np
import pandas as pd


def create_app():
    app = Flask(__name__)

    # Config Vars
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route("/")
    def home():
        return render_template('base.html', message='Spotify Recommender')

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', message='Spotify Recommender')

    @app.route('/recommend', methods=['POST'])
    def recommend():
        song_title = request.values['song_title']

        recommendations = UseSavedModel(song_title)

        return render_template('base.html',
                               message='Spotify Recommender',
                               songs=recommendations)

    return app


def UseSavedModel(track_name):
    neigh = jb.load('Spotifymodel.sav')
    track_data = get_song_DB(track_name)
    list1 = [track_data]
    track_list = [list(item) for item in list1]
    distances, song_indexes = neigh.kneighbors(track_list, 6)
    returnedlist = []
    for index in song_indexes[0]:
        returnedlist.append(get_song_from_index(index))
    return returnedlist