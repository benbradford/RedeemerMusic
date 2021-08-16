import os
import flask
import logging
from flask_talisman import Talisman
from flask_cors import CORS
from helper.log_helper import LogHelper
from logging.handlers import TimedRotatingFileHandler

logs_filename = os.path.join(os.path.dirname(__file__), '../logs/rdm_app.log')
handler = TimedRotatingFileHandler(logs_filename, when="midnight", interval=1)
handler.suffix = '%Y%m%d'
logger = logging.getLogger()
logger.setLevel('DEBUG')
logger.addHandler(handler)

templates_dir = os.path.join(os.path.dirname(__file__), '../templates/')
app = flask.Flask(__name__, template_folder=templates_dir)
log_helper = LogHelper(app.logger)
csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'lh3.googleusercontent.com',
        '*'
    ]
}
Talisman(app, content_security_policy=csp)
secrets_dir = os.path.join(os.path.dirname(__file__), '../secrets/')
with open(secrets_dir + 'app_id.txt', 'r') as file:
    app.secret_key = file.read()
CORS(app)
app.config["DEBUG"] = False
