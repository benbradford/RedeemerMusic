from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class EmailService:

    def __init__(self):
        creds = self._create_credentials()
        self._service = build('gmail', 'v1', credentials=creds)

    def send(self, message):
        return self._service.users().messages().send(userId='me', body=message).execute()

    def draft(self, message):
        return self._service.users().drafts().create(userId='me', body=message).execute()

    def _create_credentials(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../bin/token.pickle'):
            with open('../bin/token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            creds = self._login(creds)
        return creds

    def _login(self, creds):
        SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../cred/credentials_gmail.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../bin/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        return creds
