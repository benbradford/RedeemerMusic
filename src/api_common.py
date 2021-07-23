import flask
from flask_cors import CORS
from flask import request, jsonify, send_file

app = flask.Flask(__name__, template_folder='../templates')  # still relative to module
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
