import io

import json
from drive_service import DriveService

from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

driveService = DriveService()
service = driveService.get_service()

folder_id = '10_hTK6keFv1gWx-OkFuImuDtqFU8PVRN'
file_metadata = {
    'name': 'slides.txt',
    'parents': [folder_id]
}
upload = MediaFileUpload('./text_file2.txt', mimetype='text/plain' )
file = service.files().create(
    body=file_metadata,
    media_body=upload,
    fields='id',
    supportsAllDrives=True
).execute()

print file

#driveService.download_slide('1Tuw3a4Y_zCH2oL1QCxvPHJqKTYaAL7dO') #file['file_id'])
request = service.files().get_media(
    fileId=file['id'],
    supportsAllDrives=True
)
fh = io.FileIO('./downloaded.txt', mode='wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print "Download %d%%." % int(status.progress() * 100)
