import json
import base64
import os
from flask import request, jsonify, send_file

from api_common import app, extract_required_param
from service.service_factory import get_service_factory
from helper.helper_factory import get_helper_factory
from view.songs_view import SongsView
from view.song_view import SongView

songs_retriever = get_helper_factory().get_songs_retriever()
drive_service = get_service_factory().get_drive_service()
slides_helper = get_helper_factory().get_slides_helper()

@app.route('/songs', methods=['GET'])
def songs_api():
    names = songs_retriever.get_song_names()
    return SongsView().render(names)

@app.route('/song', methods=['GET'])
def song_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = songs_retriever.get_song(song_name)
    return SongView(drive_service, slides_helper).render(song)

@app.route('/test', methods=['GET'])
def test():
    drive_service.upload_slide_file('../bin/test.txt')
    return "ok"
