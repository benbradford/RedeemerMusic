import flask
import json
import base64
import os

from drive_service import DriveService
from sheets_service import SheetsService
from gmail_service import GmailService
from powerpoint import PowerpointCreator

from googleapiclient.discovery import build

from flask import request, jsonify, send_file
from flask_cors import CORS

driveService = DriveService()
sheetsService = SheetsService()
gmailService = GmailService()

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def _extract_song_param():
    if 'song' in request.args:
        return request.args['song']
    else:
        print "Error: No song field provided"
        raise "<song> is missing"

def _extract_service_param():
    if 'service' in request.args:
        return request.args['service']
    else:
        print "Error: No service field provided"
        raise "<service> is missing"

@app.route('/health', methods=['GET'])
def home():
    return "okidoki"

@app.route('/slides', methods=['GET'])
def slides_api():
    song = _extract_song_param()
    driveService.create_slides_file(song)
    songs = [song]
    ppc = PowerpointCreator(songs, '../bin/slides.pptx')
    ppc.create()
    return "ok"

@app.route('/songs', methods=['GET'])
def songs_api():
    song = _extract_song_param()
    file_ids = driveService.get_file_ids(song)
    return jsonify(file_ids)

@app.route('/services', methods=['GET'])
def services_api():
    res = sheetsService.get_services()
    services = {}
    services['services'] = res
    return jsonify(services)

@app.route('/service', methods=['GET'])
def service_api():
    service_id = _extract_service_param()
    res = sheetsService.get_service(service_id)
    if res is None:
        return {}
    return jsonify(res)

# curl -X POST -d'{"band1": "BenB_Guitar","band2": "Emma_Vox","band3": "","band4": "","band5": "","date": "Sunday 1st November","id": "2","lead": "Ben B","message": "","song1": "6","song2": "3","song3": "7","song4": "8","song5": "9","song6": "10"}' localhost:5000/service
@app.route('/service', methods=['POST'])
def add_service_api():
    new_service = request.get_json(force=True)
    if new_service is None:
        return "Error: no json body supplied"
    sheetsService.add_service(new_service)
    return "ok"

@app.route('/mail', methods=['GET'])
def send_mail_api():
    gmailService.send()
    return "ok"

app.run()
