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
        print "getting file id for " + song_name
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
        ).execute()
        items = results.get('files', [])
        if len(items) == 0:
            print "WARN Cannot find " + component + " for " + song_name
            return None
        return items[0]['id']

    def update_slide_file(self, song, lyrics):
        file_name = song['name'] + " (slides).txt"
        outF = open(file_name, "w")
        outF.write(lyrics)
        outF.write("\n")
        outF.close()

        upload = MediaFileUpload(file_name, mimetype='text/plain' )
        file = self._service.files().update(
            media_body=upload,
            fileId=song['file_ids']['slides'],
            supportsAllDrives=True
        ).execute()
        os.remove(file_name)

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
            print outfile + " - Download %d%%." % int(status.progress() * 100)

    def upload_song(self, files):
        for file in files:
            file_path = file['path']
            file_name = file_path.split('/')[1]
            file_type = file['type']
            print file_path
            print file_type
            if '(lyrics)' in file_name:
                parent = folder_ids['lyrics']
            elif '(chords)' in file_name:
                parent = folder_ids['chords']
            elif '(lead)' in file_name:
                parent = folder_ids['lead']
            elif '(slides)' in file_name:
                parent = folder_ids['slides']
                file_name = file_path.split('/')[1]
            else:
                raise("Unknown file component for " + file_name)
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
            print("Upload Complete!")

    def update_song(self, file_ids, files): # Todo this doesn't allow name changing
        for file in files:
            file_path = file['path']
            file_name = file_path.split('/')[1]
            file_type = file['type']
            print file_path
            print file_type
            file_id = None
            if '(lyrics)' in file_name:
                component = 'lyrics'
            elif '(chords)' in file_name:
                component = 'chords'
            elif '(lead)' in file_name:
                component = 'lead'
            elif '(slides)' in file_name:
                component = 'slides'
                file_name = file_path.split('/')[1]
            else:
                raise("Unknown file component for " + file_name)
            parent = folder_ids[component]
            if component in file_ids:
                file_id = file_ids[component]
            if file_id is None:
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
                print("Upload Complete!")
            else:
                upload = MediaFileUpload(file_path, mime_map[file_type] )
                file = self._service.files().update(
                    media_body=upload,
                    fileId=file_ids[component],
                    supportsAllDrives=True
                ).execute()
