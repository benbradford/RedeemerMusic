import os
import flask
from flask_talisman import Talisman
from flask_cors import CORS

templates_dir = os.path.join(os.path.dirname(__file__), '../templates/')
app = flask.Flask(__name__, template_folder=templates_dir)
csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'lh3.googleusercontent.com'
    ]
}
Talisman(app, content_security_policy=csp)
secrets_dir = os.path.join(os.path.dirname(__file__), '../secrets/')
with open(secrets_dir + 'app_id.txt', 'r') as file:
    app.secret_key = file.read()
CORS(app)
app.config["DEBUG"] = False
