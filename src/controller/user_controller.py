import os
import json
from flask import redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

secrets_dir = os.path.join(os.path.dirname(__file__), '../../secrets/')
GOOGLE_CLIENT_ID = open(secrets_dir + 'client_id.txt', 'r').read()
GOOGLE_CLIENT_SECRET = open(secrets_dir + 'client_secret.txt').read()


class UserController:
    def __init__(self, user_dao):
        self._user_dao = user_dao
        self._client = WebApplicationClient(GOOGLE_CLIENT_ID)  # TODO move to client dir

    def load_user(self, user_id):
        return self._user_dao.get(user_id)

    def login(self, google_provider_cfg, base_url):

        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = self._client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)

    def callback(self, google_provider_cfg, authorization_code_from_google, url, base_url):
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = self._client.prepare_token_request(
            token_endpoint,
            authorization_response=url,
            redirect_url=base_url,
            code=authorization_code_from_google,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )

        self._client.parse_request_body_response(json.dumps(token_response.json()))

        uri, headers, body = self._client.add_token(google_provider_cfg["userinfo_endpoint"])
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if not userinfo_response.json().get("email_verified"):
            return "User email could not be verified by Google.", 400

        user = {'id': userinfo_response.json()["sub"], 'email': userinfo_response.json()["email"],
                'pic': userinfo_response.json()["picture"], 'name': userinfo_response.json()["given_name"],
                'scope': 'rdm/all'}

        if not self._user_dao.get(user['id']):
            self._user_dao.set(user)

        login_user(user)

        return redirect(url_for("index"))

    def logout(self):
        logout_user()
        return redirect(url_for("index"))
