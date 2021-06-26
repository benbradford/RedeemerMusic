import flask
from flask_cors import CORS
from flask import request, jsonify, send_file

app = flask.Flask('Redeemer Music')
CORS(app)
app.config["DEBUG"] = True

def extract_required_param(name):
    if name in request.args:
        return request.args[name]
    else:
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
