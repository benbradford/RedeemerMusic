from service.service_factory import get_service_factory
ds = get_service_factory().get_drive_service()

songList = [

    ]

for song in songList:
    name = song['name']
    file_name = name + " (slides).txt"
    ds.upload_slide_file(file_name)
    #f = open(file_name, "r").read()
    #print f
