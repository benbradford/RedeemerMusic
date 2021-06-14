import json
import base64
from flask import request, jsonify, send_file

from api_common import app, extract_required_param
from view.songs_view import SongsView
from view.song_view import SongView
from view.edit_slides_view import EditSlidesView
from data.data_factory import get_data_factory

data_retriever = get_data_factory().get_data_retriever()
remote_data_manager = get_data_factory().get_remote_data_manager()

@app.route('/songs', methods=['GET'])
def songs_api():
    names = data_retriever.get_song_names()
    return SongsView().render(names)

@app.route('/song', methods=['GET'])
def song_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    return SongView(data_retriever).render(song)

@app.route('/refresh_slides', methods=['GET'])
def refresh_slides_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    remote_data_manager.sync_slides_for_song(song)
    return SongView(data_retriever).render(song)

@app.route('/edit_slides', methods=['GET'])
def edit_slides_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    slides = data_retriever.get_slide(song_name)
    return EditSlidesView().render(song, slides)

@app.route('/update_slides', methods=['GET'])
def update_slides_api():
    lyrics = extract_required_param('lyrics').replace("%20", " ").replace("%0D%0A", '\n')
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)

    remote_data_manager.update_slide_for_song(song, lyrics)
    return SongView(data_retriever).render(song)
