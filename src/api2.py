import flask
import json
import base64
import os

from sheets_service import SheetsService
from gmail_service import GmailService
from powerpoint import PowerpointCreator
from songs_retriever import SongsRetriever
from email_creator import EmailCreator

from googleapiclient.discovery import build

from flask import request, jsonify, send_file
from flask_cors import CORS

songsRetriever = SongsRetriever()
sheetsService = SheetsService()
gmailService = GmailService()
emailCreator = EmailCreator()

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def _extract_required_param(name):
    if name in request.args:
        return request.args[name]
    else:
        raise "Error: Missing required parameters " + name

def _extract_optional_param(name, default):
    if name in request.args:
        return request.args[name]
    else:
        return default

@app.route('/health', methods=['GET'])
def home():
    return "okidoki"

#@app.route('/slides', methods=['GET'])
#def slides_api():
#    song_name = _extract_song_param()
#    song = get_song(song_name)
#    outfile = '../bin/' + song['name'] + ' (slides).txt'
#    file_id = song['file_ids']['slides']
#    self.download_slide(file_id, out_file)
#    parsed = parser.from_file(out_file)

#    f = open("../bin/" + song + ".txt", "w")
#    slides = parsed["content"].replace(u"\u2018", "'").replace(u"\u2019", "'")
##    f.write(slides)
 ##   f.close()
#  #  driveService.create_slides_file(song)
#   # songs = [song_name]
#    #ppc = PowerpointCreator(songs, '../bin/slides.pptx')
#    ppc.create()
#    return "ok"

@app.route('/songs', methods=['GET'])
def songs_api():
    names = songsRetriever.get_song_names()
    return jsonify(names)

@app.route('/song', methods=['GET'])
def song_api():
    song_name = _extract_required_param('name')
    file_ids = songsRetriever.get_song(song_name)
    return jsonify(file_ids)

@app.route('/services', methods=['GET'])
def services_api():
    res = sheetsService.get_services()
    services = {}
    services['services'] = res
    return jsonify(services)

@app.route('/service', methods=['GET'])
def service_api():
    service_id = _extract_required_param('id')
    service = sheetsService.get_service(service_id)
    if service is None:
        return {}
    recipients = _extract_optional_param('recipients', "ben.bradford80@gmail.com")
    #'ben.bradford80@gmail.com, jonny@redeemerfolkestone.org, mark.davey9@live.co.uk, emmasarahsutton@gmail.com, elaughton7@gmail.com, ben1ayers1@gmail.com, g.yorke20@gmail.com, david.3longley@btinternet.com, chriswatkins123@gmail.com'
    return emailCreator.preview(service, recipients)

@app.route('/send_music_email', methods=['GET'])
def send_music_email_api():
    service_id = _extract_required_param('id')
    service = sheetsService.get_service(service_id)
    if service is None:
        return {}
    body = emailCreator.body(service)
    subject = emailCreator.subject(service)
    gmailService.send(subject, body, "ben.bradford80@gmail.com")
    return "ok"

# curl -X POST -d'{"band1": "BenB_Guitar","band2": "Emma_Vox","band3": "","band4": "","band5": "","date": "Sunday 1st November","id": "2","lead": "Ben B","message": "","song1": "6","song2": "3","song3": "7","song4": "8","song5": "9","song6": "10"}' localhost:5000/service
@app.route('/service', methods=['POST'])
def add_service_api():
    new_service = request.get_json(force=True)
    if new_service is None:
        return "Error: no json body supplied"
    sheetsService.add_service(new_service)
    return "ok"

app.run()
