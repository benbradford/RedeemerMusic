from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

credentials_location = os.path.join(os.path.dirname(__file__), '../../bin/')

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.compose'
]

token_path = credentials_location + "token.json"
credentials_path = credentials_location + "credentials.json"

credentials = None


def get_credentials():
    global credentials
    if credentials and credentials.valid:
        return credentials

    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(credentials.to_json())
    return credentials
