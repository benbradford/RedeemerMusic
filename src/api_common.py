import flask
from flask_cors import CORS
from flask import request, jsonify, send_file

from helper.helper_factory import init_helper_factory, get_helper_factory
from service.service_factory import get_service_factory

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

init_helper_factory(get_service_factory())

def extract_required_param(name):
    if name in request.args:
        return request.args[name]
    else:
        print "Error: Missing required parameters " + name
        raise "Error: Missing required parameters "

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
