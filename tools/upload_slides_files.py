from client.client_factory import get_client_factory
ds = get_client_factory().get_drive_client()

songList = [

    ]

for song in songList:
    name = song['name']
    file_name = name + " (slides).txt"
    ds.upload_slide_file(file_name)
    #f = open(file_name, "r").read()
    #print f
