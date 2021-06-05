from __future__ import print_function

import io

import tika
tika.initVM()
from tika import parser

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from credentials import get_credentials

class DriveService:

    def __init__(self):
        self._service = build('drive', 'v3', credentials=get_credentials())

    def get_file_ids(self, song):
        file_ids = {}
        self._add_file_details(file_ids, song, 'lyrics')
        self._add_file_details(file_ids, song, 'chords')
        self._add_file_details(file_ids, song, 'lead')
        self._add_file_details(file_ids, song, 'slides')
        return file_ids

    def create_slides_file(self, song):
        file_id = self._get_file_id(song, 'slides')
        request = self._service.files().export_media(fileId=file_id, mimeType='application/vnd.oasis.opendocument.text')
        fh = io.FileIO('../bin/slides.doc', mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        parsed = parser.from_file('../bin/slides.doc')

        f = open("../bin/" + song + ".txt", "w")
        slides = parsed["content"].replace(u"\u2018", "'").replace(u"\u2019", "'")
        f.write(slides)
        f.close()

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
