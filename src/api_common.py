import flask
from flask_cors import CORS
from flask import request, jsonify, send_file

from client.client_factory import get_client_factory
from data.data_factory import get_data_factory, init_data_factory

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

init_data_factory(
    get_client_factory().get_drive_client(),
    get_client_factory().get_sheets_client()
)

def extract_required_param(name):
    if name in request.args:
        return request.args[name]
    else:
        print "Error: Missing required parameters " + name
        raise Exception("Error: Missing required parameters ")

def extract_optional_param(name, default):
    if name in request.args:
        return request.args[name]
    else:
        return default

def extract_body_from_request():
    body = request.get_json(force=True)
    if body is None:
        return "Error: no json body supplied"
    return body
