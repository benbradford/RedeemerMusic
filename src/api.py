import flask
from flask import request, jsonify
import json
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64

from json_pp_creator import create_pp
from email_service import EmailService

ok = [200]

def _get_service(request):
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    filename = '../services/'
    filename += id.split('_')[0] + "/"
    filename += id
    service = open(filename, "r").read()
    return json.loads(service)

def _get_songs():
    songsstring = open('../res/songs.json', "r").read()
    return json.loads(songsstring)

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Test page</h1><p>This route is unused</p>"

@app.route('/songs', methods=['GET'])
def songs():
    return jsonify(_get_songs())

@app.route('/service', methods=['GET'])
def service():
    return jsonify(_get_service(request))

@app.route('/powerpoint', methods=['GET'])
def powerpoint():
    service = _get_service(request)
    songs = _get_songs()
    result = []
    for song in service['songs']:
        for test in songs['songList']:
            if test['id'] == song:
                pp_file = ""
                if 'ppt' in test:
                    pp_file = test['ppt']
                else:
                    pp_file = 'res/ppt/' + test['id'] + '.txt'
                pp_file = '../' + pp_file
                pp_file = pp_file.replace('.txt', '.json')
                pp = open(pp_file, "r").read()
                pp_json = json.loads(pp)
                print (jsonify(pp))
                result.append(pp_json)
    created_pp = create_pp(result)
    all = {}
    all['res'] = result

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
    EmailService().send(raw_message)

    return jsonify(all)
app.run()
