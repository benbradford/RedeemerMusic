import os
import json
from flask import redirect
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from user import User

secrets_dir = os.path.join(os.path.dirname(__file__), '../../secrets/')
with open(secrets_dir + 'client_id.txt', 'r') as file:
    GOOGLE_CLIENT_ID = file.read()
with open(secrets_dir + 'client_secret.txt', 'r') as file:
    GOOGLE_CLIENT_SECRET = file.read()


class UserController:
    def __init__(self, logger, user_dao):
        self._user_dao = user_dao
        self._client = WebApplicationClient(GOOGLE_CLIENT_ID)
        self._logger = logger

    def load_user(self, user_id):
        return User(self._user_dao.get(user_id))

    def login(self, google_provider_cfg, base_url):
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = self._client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=base_url + "/login/callback",
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
                'scope': User.get_default_scope()}
        if self._user_dao.get(user['id']) is None:
            self._user_dao.set(user)

        user_to_login = User(user)
        self._logger.get_for(user_to_login).info("UserController: Attempting log in for " + user['name'])
        login_user(user_to_login, remember=True)
        self._logger.get_for(user_to_login).info("UserController: Login success ")

        return redirect(url.replace('login/callback', 'home'))

    def logout(self, url):
        self._logger.get().info("UserController: Logging out")
        logout_user()
        return redirect(url)
