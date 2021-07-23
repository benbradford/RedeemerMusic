import os
from sys import path
from os.path import dirname as dir
path.append(dir(path[0]) + '/src')

import flask
from flask_cors import CORS
from flask import request, jsonify, send_file

app = flask.Flask('Redeemer Music')
CORS(app)
app.config["DEBUG"] = True

from client.client_factory import get_client_factory
client = get_client_factory().get_drive_client()

def get_song_from_params(component, files):
    uploaded_file = request.files[component]
    if uploaded_file.filename != '':
        type = uploaded_file.filename.split('.')[1]
        file_name = uploaded_file.filename.split('.')[0]
        if '(slides)' in file_name:
            file_name = file_name + '.txt'
        out_path = 'bin/' + file_name
        uploaded_file.save(out_path)
        files.append({'path': out_path, 'type': type})

@app.route('/test', methods=['GET'])
def home():
    return open('tools/upload_song.html', "r").read()

@app.route('/upload_song', methods=['POST'])
def up_api():
    files = []
    get_song_from_params('lyrics', files)
    get_song_from_params('lead', files)
    get_song_from_params('chords', files)
    get_song_from_params('slides', files)
    client.upload_song(files)
    return "ok"

app.run()
