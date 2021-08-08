import os
import flask
from flask import render_template, redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)

from flask_cors import CORS
from flask import request
import requests

from client.client_factory import get_client_factory
from data.data_factory import init_data_factory, get_data_factory
from data.db_init import init_db
from helper.slides_helper import SlidesHelper
from controller.song_controller import SongController
from controller.user_controller import UserController
from controller.service_controller import ServiceController
from controller.recipients_controller import RecipientsController

app = flask.Flask(__name__, template_folder='../templates')  # still relative to module
app.secret_key = 'abcdefghijklmnopqrstuvwx'
CORS(app)
app.config["DEBUG"] = False
login_manager = LoginManager()
login_manager.init_app(app)

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

init_db()

init_data_factory(
    get_client_factory().get_drive_client(),
    get_client_factory().get_sheets_client()
)

song_controller = SongController(get_data_factory().get_songs_dao())
user_controller = UserController(get_data_factory().get_user_dao())
service_controller = ServiceController(get_client_factory().get_gmail_client(),
                                       get_data_factory().get_service_dao(),
                                       get_data_factory().get_songs_dao(),
                                       SlidesHelper(get_data_factory().get_songs_dao()),
                                       get_data_factory().get_recipient_dao(),
                                       get_data_factory().get_band_dao())
recipients_controller = RecipientsController(get_data_factory().get_recipient_dao())


def extract_required_param(name):
    if name in request.args:
        return request.args[name]
    else:
        raise Exception("Error: Missing required parameters ")


@app.route('/health', methods=['GET'])
def health(): return "okidoki"


@app.route('/', methods=['GET'])
def index(): return redirect(url_for('home_api'), code=302)


@app.route('/home', methods=['GET'])
def home_api(): return render_template('home.html')


@app.route('/about', methods=['GET'])
def about_api(): return render_template('about.html')


@app.route('/songs', methods=['GET'])
def songs_api(): return song_controller.show_songs_page()

@app.route('/song', methods=['GET'])
def song_api(): return song_controller.show_song_page(extract_required_param('name'))


@app.route('/edit_slides', methods=['GET'])
def edit_slides_api(): return song_controller.show_edit_slides_page(extract_required_param('name'))


@app.route('/update_slides', methods=['GET'])
def update_slides_api(): return song_controller.update_slides(extract_required_param('name'),
                                                              extract_required_param('lyrics')
                                                              .replace("%20", " ").replace("%0D%0A", '\n'))


@app.route('/add_song_page', methods=['GET'])
def add_song_page_api(): return song_controller.show_add_song_page()


@app.route('/add_song', methods=['POST'])
def add_song_api(): return song_controller.add_song(request.form.get('name'), request.form.get('ccli'), request.files)


@app.route('/update_song_page', methods=['GET'])
def update_song_page_api(): return song_controller.show_update_song_page(extract_required_param('name'))


@app.route('/update_song', methods=['POST'])
def update_song_api(): return song_controller.update_song(request.form.get('name'),
                                                          request.form.get('previous'),
                                                          request.files)


@app.route('/services', methods=['GET'])
def services_api(): return service_controller.show_services_page()


@app.route("/add_service_page", methods=['GET'])
def add_service_page_api(): return service_controller.show_add_service_page()


@app.route("/add_service", methods=['GET'])
def add_service_api(): return service_controller.add_service(request.args)


@app.route('/service', methods=['GET'])
def service_api(): return service_controller.show_service(extract_required_param('id'))


@app.route('/edit_service', methods=['GET'])
def edit_service_api(): return service_controller.show_edit_service_page(extract_required_param('id'))


@app.route('/update_service', methods=['GET'])
def update_service_api(): return service_controller.update_service(extract_required_param('id'), request.args)


@app.route('/send_music_email', methods=['GET'])
def send_music_email_api(): return service_controller.send_music_email(extract_required_param('id'),
                                                                       extract_required_param('recipients'))


@app.route('/email_slides', methods=['GET'])
def email_slides_api(): return service_controller.send_slides_email(extract_required_param('id'),
                                                                    extract_required_param('recipients'))


@app.route('/preview_slides', methods=['GET'])
def preview_slides_api(): return service_controller.preview_slides(extract_required_param('id'))


@app.route('/recipients', methods=['GET'])
def recipients_api(): return recipients_controller.show_recipients_page()


@app.route('/add_recipient_page', methods=['GET'])
def add_recipient_page_api(): return recipients_controller.show_add_new_page()


@app.route('/add_recipient', methods=['POST'])
def add_recipient_api(): return recipients_controller.add_new(request.form)


@app.route('/add_recipient_register', methods=['GET'])
def add_recipient_register_api(): return recipients_controller.add_recipient_register(
    extract_required_param('email'),
    extract_required_param('register_index'))


@app.route('/remove_recipient_register', methods=['GET'])
def remove_recipient_register_api(): return recipients_controller.remove_recipient_register(
    extract_required_param('email'),
    extract_required_param('register_index'))


@login_manager.unauthorized_handler
def unauthorized(): return "You must be logged in to access this content.", 403


@login_manager.user_loader
def load_user(user_id): return user_controller.load_user(user_id)


@app.route("/login")
def login(): return user_controller.login(requests.get(GOOGLE_DISCOVERY_URL).json(), 'https://localhost')


@app.route("/login/callback")
def callback(): return user_controller.callback(requests.get(GOOGLE_DISCOVERY_URL).json(),
                                                request.args.get("code"),
                                                'https' + request.url[4:],
                                                'https' + request.base_url[4:])


@app.route("/logout")
@login_required
def logout(): return user_controller.logout()
