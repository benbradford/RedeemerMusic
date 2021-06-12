import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from sheets_client import SheetsClient
from gmail_client import GmailClient
from drive_client import DriveClient


SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.compose'
]

class ClientFactory:
    def __init__(self):
        self._credentials=self._get_credentials()
        self._drive_client = None
        self._sheets_client = None
        self._gmail_client = None

    def get_drive_client(self):
        if self._drive_client == None:
            self._drive_client = DriveClient(self._credentials)
        return self._drive_client

    def get_sheets_client(self):
        if self._sheets_client is None:
            self._sheets_client = SheetsClient(self._credentials)
        return self._sheets_client

    def get_gmail_client(self):
        if self._gmail_client is None:
            self._gmail_client = GmailClient(self._credentials)
        return self._gmail_client

    def _get_credentials(self):
        creds = None

        if os.path.exists('../bin/token.json'):
            creds = Credentials.from_authorized_user_file('../bin/token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../bin/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../bin/token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

client_factory = ClientFactory()

def get_client_factory():
    return client_factory
