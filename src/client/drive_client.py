import io
import os
from operator import itemgetter

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

from credentials import get_credentials

folder_ids = {
    'lyrics': '1A0u-Fixg4uEjipe8ZL7rWoPg7E86cS5b',
    'chords': '13G13PpGFPeSmMI6YEjXiBwi7VYVYQMm8',
    'lead': '1PnliQdA9zmuu2s0n9PAzFbzz1JfLb6Hv',
    'slides': '10_hTK6keFv1gWx-OkFuImuDtqFU8PVRN'
}

mime_map = {
    'pdf': 'application/pdf',
    'txt': 'text/plain'
}

class DriveClient:

    def __init__(self, creds):
        self._service = build('drive', 'v3', credentials=creds)

    def list_files(self, component):
        print ("getting services")
        folder_id = folder_ids[component]
        items = []
        page_token = None
        while True:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            param['q'] = "'" + folder_id + "' in parents"
            param['pageSize']=10
            param['fields']="nextPageToken, files(id, name)"
            param['includeItemsFromAllDrives']=True
            param['supportsAllDrives']=True
            files = self._service.files().list(
                **param
            ).execute()

            items.extend(files.get('files', []))

            page_token = files.get('nextPageToken')
            if not page_token:
                items.sort(key=itemgetter("name"))
                return items


    def get_file_id(self, song_name, component):
        folder_id = folder_ids[component]
        print ("getting " + component + " file id for " + song_name)
        song_file_name = song_name + " (" + component + ")"
        song_file_name = song_file_name.replace("'", "\\'")
        if component == 'slides':
            song_file_name += ".txt"
        results = self._service.files().list(
            pageSize=5,
            fields="nextPageToken, files(id, name)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            q="name ='" + song_file_name + "' and '" + folder_id + "' in parents"
        ).execute() # TODO httplib2.Http() https://stackoverflow.com/questions/50172034/google-drive-multythreading-move-files-python
        items = results.get('files', [])
        if len(items) == 0:
            print ("WARN Cannot find " + component + " for " + song_name)
            return None
        return items[0]['id']

    def download_slide(self, file_id, outfile):
        request = self._service.files().get_media(
            fileId=file_id,
            supportsAllDrives=True
        )
        fh = io.FileIO(outfile, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print (outfile + " - Download %d%%." % int(status.progress() * 100))

    def add_song_component(self, component, file_path, file_name, file_type):
        parent = folder_ids[component]
        media = MediaFileUpload(
            file_path,
            mimetype=mime_map[file_type],
            resumable=True
        )
        request = self._service.files().create(
            media_body=media,
            supportsAllDrives=True,
            body={'name': file_name, 'parents': [parent]}
        )
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))
        print("Upload Completed! file id is " + response['id'])
        return response['id']

    def update_song_component(self, component, file_path, file_name, file_type, file_id): # Todo this doesn't allow name changing
        if file_id is None:
            return self.add_song_component(component, file_path, file_name, file_type)
        else:
            parent = folder_ids[component]
            upload = MediaFileUpload(file_path, mime_map[file_type] )
            file = self._service.files().update(
                media_body=upload,
                fileId=file_id,
                supportsAllDrives=True
            ).execute()
            return file_id
