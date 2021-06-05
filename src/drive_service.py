from __future__ import print_function
import os.path
import io

import tika
tika.initVM()
from tika import parser

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.metadata']

service = None

class DriveService:

    def __init__(self):
        self._service = self._get_service()

    def get_file_ids(self, song):
        file_ids = {}
        self._add_file_details(file_ids, song, 'lyrics')
        self._add_file_details(file_ids, song, 'chords')
        self._add_file_details(file_ids, song, 'lead')
        self._add_file_details(file_ids, song, 'slides')
        return file_ids

    def get_slides(self, song):
        file_id = self._get_file_id(song, 'slides')
        request = self._service.files().export_media(fileId=file_id, mimeType='application/vnd.oasis.opendocument.text')
        fh = io.FileIO('../bin/slides.doc', mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        parsed = parser.from_file('../bin/slides.doc')

        slides = {}
        slides['text'] = parsed["content"]
        return slides

    def _add_file_details(self, file_ids, song, type):
        try:
            id = self._get_file_id(song, type)
            file_ids[type] = id
        except:
            print("[WARN] Cannot find " + type + " for " + song)

    def _get_file_id(self, song, type):
        # Call the Drive v3 API
        results = self._service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            q="name contains '" + song + " (" + type + ")'"
        ).execute()
        items = results.get('files', [])
        return items[0]['id']

    def _get_service(self):
        creds = self._get_drive_credentials()
        service = build('drive', 'v3', credentials=creds)
        return service

    def _get_drive_credentials(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../bin/token.json'):
            creds = Credentials.from_authorized_user_file('../bin/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
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
