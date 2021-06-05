import flask
import json
import base64
import os

from drive_service import DriveService

from googleapiclient.discovery import build

from flask import request, jsonify, send_file
from flask_cors import CORS

driveService = DriveService()

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def _extract_song_param():
    if 'song' in request.args:
        return request.args['song']
    else:
        print "Error: No song field provided"
        raise "Song is missing"

@app.route('/health', methods=['GET'])
def home():
    return "okidoki"

@app.route('/slides', methods=['GET'])
def slides_api():
    song = _extract_song_param()
    slides = driveService.get_slides(song)
    return slides

@app.route('/songs', methods=['GET'])
def songs_api():
    song = _extract_song_param()
    file_ids = driveService.get_file_ids(song)
    return jsonify(file_ids)

app.run()
