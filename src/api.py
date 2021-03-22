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

def _get_slides(id):
    song = _get_song(id)[0]
    if 'name' not in song:
        return "Error: no name in song"
    print song['name']
    ppt_file = '../res/slides/' + song['name'] + '.json'
    file = open(ppt_file, "r").read()
    return json.loads(file)

def _get_songs():
    songsstring = open('../res/songs.json', "r").read()
    return json.loads(songsstring)

def _get_powerpoint_paths(request):
    service = _get_service(request)
    songs = _get_songs()
    result = []
    for song in service['songs']:
        for test in songs['songList']:
            if test['id'] == song:
                ppt_file = '../res/slides/' + test['name'] + '.json'
                pp = open(ppt_file, "r").read()
                pp_json = json.loads(pp)
                print (jsonify(pp))
                result.append(pp_json)
    return result

def _update_song(old_song, new_song, key):
    if key in new_song:
        old_song[key] = new_song[key]
    return new_song

def _get_services():
    services = {}
    services['services'] = []
    for year_folder in os.listdir('../services'):
        for service_file in os.listdir('../services/' + year_folder):
            service = open('../services/' + year_folder + '/' + service_file, "r").read()
            services['services'].append(json.loads(service));
    return services

def _get_service(request):
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    id = int(request.args['id'])
    services = _get_services()
    for service in services['services']:
        if service['id'] == id:
            return service
    return "Error: could not find service"

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
    return jsonify(_get_service(request))

# ?id=<service_id>
@app.route('/sendpowerpoint', methods=['GET'])
def send_powerpoint():
    songs_to_use = _get_powerpoint_paths(request)
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
    return jsonify(songs)

@app.route('/add_slides', methods=['POST'])
def add_slides():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    id = id.replace('_', ' ')
    slides = request.get_json(force=True)
    if slides is None:
        return "Error: no json body supplied"
    if 'slides' in slides is None:
        return "Error: no slides in json"

    song = _get_song(id)[0]

    ppt_file = '../res/slides/' + song['name'] + '.json'
    with open(ppt_file, 'w+') as f:
        json.dump(slides, f)
    return slides

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
        print m
        if m['id'] == new_member['id']:
            return "Error: member id already exists"
    members['members'].append(new_member)
    return jsonify(members)

app.run()
