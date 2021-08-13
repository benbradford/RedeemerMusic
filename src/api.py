from flask import render_template, redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)
from flask import request
import requests

from init_app import app
from client.client_factory import get_client_factory
from data.data_factory import init_data_factory, get_data_factory
from data.db_init import init_db
from helper.slides_helper import SlidesHelper
from controller.controller_factory import ControllerFactory
from controller.song_controller import SongController
from controller.user_controller import UserController
from controller.service_controller import ServiceController
from controller.recipients_controller import RecipientsController
from controller.admin_controller import AdminController

login_manager = LoginManager()
login_manager.init_app(app)

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

init_db()

init_data_factory(
    get_client_factory().get_drive_client(),
    get_client_factory().get_sheets_client()
)

song_factory = ControllerFactory(SongController, get_data_factory().get_songs_dao())
user_controller = UserController(get_data_factory().get_user_dao())
service_factory = ControllerFactory(ServiceController, {'gmail_client': get_client_factory().get_gmail_client(),
                                        'service_dao': get_data_factory().get_service_dao(),
                                        'songs_dao': get_data_factory().get_songs_dao(),
                                        'slides_helper': SlidesHelper(get_data_factory().get_songs_dao()),
                                        'recipients_dao': get_data_factory().get_recipient_dao(),
                                        'band_dao': get_data_factory().get_band_dao()})
recipients_factory = ControllerFactory(RecipientsController, get_data_factory().get_recipient_dao())
admin_factory = ControllerFactory(AdminController, get_data_factory().get_user_dao())


@app.route('/health', methods=['GET'])
def health(): return "okidoki"


@app.route('/', methods=['GET'])
def index(): return redirect(url_for('home_api'), code=302)


@app.route('/home', methods=['GET'])
def home_api(): return render_template('home.html', user=current_user)


@app.route('/about', methods=['GET'])
def about_api(): return render_template('about.html', user=current_user)


@app.route('/songs', methods=['GET'])
def songs_api(): return song_factory.get(current_user).show_songs_page()


@app.route('/song', methods=['GET'])
def song_api(): return song_factory.get(current_user).show_song_page(request.args['name'])


@app.route('/edit_slides', methods=['GET'])
def edit_slides_api(): return song_factory.get(current_user).show_edit_slides_page(request.args['name'])


@app.route('/update_slides', methods=['GET'])
def update_slides_api(): return song_factory.get(current_user).update_slides(request.args['name'],
                                                                             request.args['lyrics']
                                                                             .replace("%20", " ").replace("%0D%0A",
                                                                                                          '\n'))


@app.route('/add_song_page', methods=['GET'])
def add_song_page_api(): return song_factory.get(current_user).show_add_song_page()


@app.route('/add_song', methods=['POST'])
def add_song_api(): return song_factory.get(current_user).add_song(request.form.get('name'), request.form.get('ccli'),
                                                                   request.files)


@app.route('/update_song_page', methods=['GET'])
def update_song_page_api(): return song_factory.get(current_user).show_update_song_page(request.args['name'])


@app.route('/update_song', methods=['POST'])
def update_song_api(): return song_factory.get(current_user).update_song(request.form.get('name'),
                                                                         request.form.get('previous'),
                                                                         request.files)


@app.route('/services', methods=['GET'])
def services_api(): return service_factory.get(current_user).show_services_page()


@app.route("/add_service_page", methods=['GET'])
def add_service_page_api(): return service_factory.get(current_user).show_add_service_page()


@app.route("/add_service", methods=['GET'])
def add_service_api(): return service_factory.get(current_user).add_service(request.args)


@app.route('/service', methods=['GET'])
def service_api(): return service_factory.get(current_user).show_service(request.args['id'])


@app.route('/edit_service', methods=['GET'])
def edit_service_api(): return service_factory.get(current_user).show_edit_service_page(request.args['id'])


@app.route('/update_service', methods=['GET'])
def update_service_api(): return service_factory.get(current_user).update_service(request.args['id'], request.args)


@app.route('/send_music_email', methods=['GET'])
def send_music_email_api(): return service_factory.get(current_user).send_music_email(request.args['id'], request.args['recipients'])


@app.route('/email_slides', methods=['GET'])
def email_slides_api(): return service_factory.get(current_user).send_slides_email(request.args['id'], request.args['recipients'])


@app.route('/preview_slides', methods=['GET'])
def preview_slides_api(): return service_factory.get(current_user).preview_slides(request.args['id'])


@app.route('/recipients', methods=['GET'])
def recipients_api(): return recipients_factory.get(current_user).show_recipients_page()


@app.route('/add_recipient_page', methods=['GET'])
def add_recipient_page_api(): return recipients_factory.get(current_user).show_add_new_page()


@app.route('/add_recipient', methods=['POST'])
def add_recipient_api(): return recipients_factory.get(current_user).add_new(request.form)


@app.route('/add_recipient_register', methods=['GET'])
def add_recipient_register_api(): return recipients_factory.get(current_user).add_recipient_register(
    request.args['email'],
    request.args['register_index'])


@app.route('/remove_recipient_register', methods=['GET'])
def remove_recipient_register_api(): return recipients_factory.get(current_user).remove_recipient_register(
    request.args['email'],
    request.args['register_index'])


@app.route('/users_edit', methods=['GET'])
def users_edit_page_api(): return admin_factory.get(current_user).show_users_edit_page()


@app.route('/update_user', methods=['POST'])
def update_user_api(): return admin_factory.get(current_user).update_user(request.form.get('id'),
                                                                          request.form.get('scope'))


@login_manager.unauthorized_handler
def unauthorized(): return "You must be logged in to access this content.", 403


@login_manager.user_loader
def load_user(user_id): return user_controller.load_user(user_id)


@app.route("/login")
def login():
    host_url = request.host_url.replace('http', 'https')[:-1]
    print "redirect to " + host_url
    print str(request.headers)
    for r in request.headers:
        print str(r)
    return user_controller.login(requests.get(GOOGLE_DISCOVERY_URL).json(), host_url)


@app.route("/login/callback")
def callback(): return user_controller.callback(requests.get(GOOGLE_DISCOVERY_URL).json(),
                                                request.args.get("code"),
                                                request.url.replace('http', 'https'),
                                                request.base_url.replace('http', 'https'))


@app.route("/logout")
def logout(): return UserController.logout(request.url.replace('http', 'https').replace('logout', 'home'))
