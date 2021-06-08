import json
import base64
import os
from flask import request, jsonify, send_file

from api_common import app, extract_required_param
from service.service_factory import get_service_factory
from helper.helper_factory import get_helper_factory
from display.song_picker import SongPicker

songs_retriever = get_helper_factory().get_songs_retriever()

@app.route('/songs', methods=['GET'])
def songs_api():
    names = songs_retriever.get_song_names()
    return SongPicker().display(names)

@app.route('/song', methods=['GET'])
def song_api():
    song_name = extract_required_param('name')
    file_ids = songs_retriever.get_song(song_name)
    return jsonify(file_ids)
