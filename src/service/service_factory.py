import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from service.sheets_service import SheetsService
from service.gmail_service import GmailService
from service.drive_service import DriveService


SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.compose'
]

class ServiceFactory:
    def __init__(self):
        self._credentials=self._get_credentials()
        self._drive_service = None
        self._sheets_service = None
        self._gmail_service = None

    def get_drive_service(self):
        if self._drive_service == None:
            self._drive_service = DriveService(self._credentials)
        return self._drive_service

    def get_sheets_service(self):
        if self._sheets_service is None:
            self._sheets_service = SheetsService(self._credentials)
        return self._sheets_service

    def get_gmail_service(self):
        if self._gmail_service is None:
            self._gmail_service = GmailService(self._credentials)
        return self._gmail_service

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

service_factory = ServiceFactory()

def get_service_factory():
    return service_factory
