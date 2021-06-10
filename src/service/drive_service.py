import io
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

class DriveService:

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

    def upload_slide_file(self, filename):
        file_metadata = {
            'name': filename,
            'parents': [folder_ids['slides']]
        }
        upload = MediaFileUpload(filename, mimetype='text/plain' )
        file = self._service.files().create(
            body=file_metadata,
            media_body=upload,
            fields='id',
            supportsAllDrives=True
        ).execute()

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
            print "Download %d%%." % int(status.progress() * 100)
