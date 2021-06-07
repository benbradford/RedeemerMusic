import io

import json
from drive_service import DriveService

from googleapiclient.http import MediaIoBaseDownload

driveService = DriveService()
service = driveService.get_service()

mimes = {
    "document": "application/vnd.google-apps.document",
    "file": "application/vnd.google-apps.file"
}

components = ['lyrics', 'chords', 'lead']

songsstring = open('./songs.json', "r").read()
songs_from_file = json.loads(songsstring)

songs = []

folder_ids = {
    'lyrics': '1A0u-Fixg4uEjipe8ZL7rWoPg7E86cS5b',
    'chords': '13G13PpGFPeSmMI6YEjXiBwi7VYVYQMm8',
    'lead': '1PnliQdA9zmuu2s0n9PAzFbzz1JfLb6Hv',
    'slides': '10_hTK6keFv1gWx-OkFuImuDtqFU8PVRN'
}

def _find_file(file_id, name, mime):
    print "looking for"
    print file_id
    file = service.files().get(
        fileId=file_id,
        supportsAllDrives=True
    ).execute()

    return file

def _find_file_for_component(res, song, component):
    if component in song:
        name = song['name'] + component
        mime = mimes[song[component]['type']]
        res[component] = _find_file(song[component]['file_id'], name, mime)

def _find_files(song):
    res = {}
    _find_file_for_component(res, song, 'lyrics')
    _find_file_for_component(res, song, 'chords')
    _find_file_for_component(res, song, 'lead')
    print res
    return res;

def _get_type_and_id(song, song_from_file, component):
    if component in song_from_file:
        split = song_from_file[component].split('/')
        res = {}
        res['type'] = split[3]
        res['file_id'] = split[5]
        song[component] = res

for i, song_from_file in enumerate(songs_from_file['songList']):
    song = {}
    song['name'] = song_from_file['name']
    _get_type_and_id(song, song_from_file, 'lyrics')
    _get_type_and_id(song, song_from_file, 'chords')
    _get_type_and_id(song, song_from_file, 'lead')

    songs.append(song)
for song in songs:
    #song = songs[0]
    file_details = _find_files(song)
    for component in components:
        if component in song:
            file_name = song['name'] + ' (' + component + ')'
            service.files().update(
                fileId=song[component]['file_id'],
                supportsAllDrives=True,
                body={"name": file_name}
            ).execute()


#file_id = songs[0]['lyrics']['file_id']
#new_lyrics_name = songs[0]['name'] + " (lyrics)"
#file = file_details['lyrics']
#file['title'] = new_lyrics_name

#mime = file['mimeType']
#del file['id']  # 'id' has to be deleted
#print file

#media_body = MediaFileUpload(
#    new_lyrics_name, mimetype=mime, resumable=True)

#print body

# Send the request to the API.
#updated_file = service.files().update(
#    fileId=file_id,
#    body=file,
#    newRevision=new_revision,
#    media_body=media_body
#).execute()


#service.files().update().execute()
#print file
