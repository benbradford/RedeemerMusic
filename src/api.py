import flask
import json
import mimetypes
import base64
import os

from flask import request, jsonify
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from json_pp_creator import create_pp
from email_service import EmailService


def _get_song(id):
    id = int(id)
    songs = json.loads(open('../res/songs.json', "r").read())
    for i, song in enumerate(songs['songList']):
        if song['id'] == id:
            return song, i
    return {}, -1

def _get_presentations():
    file = open('../res/presentations.json', "r").read()
    return json.loads(file)

def _get_slides(id):
    id = int(id)
    presentations = _get_presentations()
    for p in presentations['presentations']:
        if p['id'] == id:
            return p
    return "Error: Cannot get slides for " + str(id)


def _get_songs():
    songsstring = open('../res/songs.json', "r").read()
    return json.loads(songsstring)

def _get_powerpoint_paths(service_id):
    service = _get_service(service_id)
    result = []
    for song_id in service['songs']:
        result.append(_get_slides(song_id))
    return result

def _update_song(old_song, new_song, key):
    if key in new_song:
        old_song[key] = new_song[key]
    return new_song

def _get_services():
    services = open('../res/services.json', "r").read()
    return json.loads(services)

def _get_service(id):
    id = int(request.args['id'])
    services = _get_services()
    for service in services['services']:
        if service['id'] == id:
            return service
    return "Error: could not find service"

def _write_songs(songs):
    with open('../res/songs.json', 'w+') as f:
        json.dump(songs, f, indent=4, sort_keys=True)

def _write_services(services):
    with open('../res/services.json', 'w+') as f:
        json.dump(services, f, indent=4, sort_keys=True)

def _write_members(members):
    with open('../res/members.json', 'w+') as f:
        json.dump(members, f, indent=4, sort_keys=True)

def _validate_service(service):
    if 'band' not in service:
        return "Error: no band"
    if 'date' not in service:
        return "Error: no date"
    if 'lead' not in service:
        return "Error: no lead"
    if 'songs' not in service:
        return "Error: no songs"
    for song in service['songs']:
        if _get_song(song)[1] == -1:
            return "Error: cannot find song " + str(song)
    return None

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Test page</h1><p>This route is unused</p>"

@app.route('/songs', methods=['GET'])
def songs():
    return jsonify(_get_songs())

@app.route('/song', methods=['GET'])
def song():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    return jsonify(_get_song(id)[0])

@app.route('/services', methods=['GET'])
def services():
    return jsonify(_get_services())

# ?id=<service-id>
@app.route('/service', methods=['GET'])
def service():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    return jsonify(_get_service(id))

# ?id=<service_id>
@app.route('/sendpowerpoint', methods=['GET'])
def send_powerpoint():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    songs_to_use = _get_powerpoint_paths(id)
    created_pp = create_pp(songs_to_use)

    message = MIMEMultipart()
    message.attach(MIMEText("<p> test message </p>", "html"))
    message['to'] = 'ben.bradford80@gmail.com'
    message['from'] = base64.urlsafe_b64encode('ben.bradford80@gmail.com')
    message['subject'] = 'Powerpoint test'

    outfile = '../bin/_outFile.pptx'

    with open(outfile, "rb") as fil:
        part = MIMEApplication( fil.read(), Name='_outFile.pptx')
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="_outFile.pptx"'
        message.attach(part)

    raw_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
    # EmailService().send(raw_message)

    result = {}
    result['res'] = songs_to_use
    return jsonify(result)

@app.route('/add_service', methods=['POST'])
def add_service():
    songs = _get_songs()
    new_service = request.get_json(force=True)
    if new_service is None:
        return "Error: no json body supplied"
    if 'key' in new_service:
        return "Error: id should not be supplied"

    error = _validate_service(new_service)
    if error:
        return error

    services = _get_services()
    new_service['id'] = len(services['services'])
    services['services'].append(new_service)
    _write_services(services)
    return jsonify(services)

@app.route('/update_service', methods=['POST'])
def update_service():
    songs = _get_songs()
    new_service = request.get_json(force=True)
    if new_service is None:
        return "Error: no json body supplied"
    if 'id' not in new_service:
        return "Error: no id supplied"

    error = _validate_service(new_service)
    if error:
        return error

    services = _get_services()
    index = -1
    for i, service in enumerate(services['services']):
        if service['id'] == new_service['id']:
            index = i
            break
    if index == -1:
        return "Error: could not find service"

    services['services'].pop(index)
    services['services'].append(new_service)
    _write_services(services)
    return jsonify(services)

@app.route('/add_song', methods=['POST'])
def add_song():
    songs = _get_songs()
    new_song = request.get_json(force=True)
    if new_song is None:
        return "Error: no json body supplied"

    if 'name' not in new_song:
        return "Error: no song name"

    for song in songs['songList']:
        if (song['name'] == new_song['name']):
            return "Error: song already exists"

    new_song['id'] = len(songs['songList'])
    songs['songList'].append(new_song)
    _write_songs(songs)
    return jsonify(songs)

@app.route('/update_song', methods=['PUT'])
def update_song():
    songs = _get_songs()
    new_song = request.get_json(force=True)
    if new_song is None:
        return "Error: no json body supplied"
    if 'id' not in new_song:
        return "Error: no id in body"
    song, index = _get_song(new_song['id'])
    if song is None:
        return "Error: song does not exist"
    songs['songList'].pop(index)
    for key in new_song.keys():
        _update_song(song, new_song, key)
    songs['songList'].append(song)
    _write_songs(songs)
    return jsonify(songs)

@app.route('/add_slides', methods=['POST'])
def add_slides():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    slides = request.get_json(force=True)
    if slides is None:
        return "Error: no json body supplied"
    if 'slides' in slides is None:
        return "Error: no slides in json"

    return "Error: not implemented"

@app.route('/get_slides', methods=['GET'])
def get_slides():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    slides = _get_slides(id)
    return jsonify(slides)

@app.route('/members', methods=['GET'])
def get_members():
    file = open('../res/members.json', "r").read()
    return file

@app.route('/add_member', methods=['POST'])
def add_member():
    new_member = request.get_json(force=True)
    if new_member is None:
        return "Error: no json body supplied"
    if 'id' not in new_member:
        return "Error: no id"
    if 'name' not in new_member:
        return "Error: no name"
    if 'instrument' not in new_member:
        return "Error: no instrument"
    file = open('../res/members.json', "r").read()
    members = json.loads(file)
    for m in members['members']:
        if m['id'] == new_member['id']:
            return "Error: member id already exists"
    members['members'].append(new_member)
    _write_members(members)
    return jsonify(members)

app.run()
