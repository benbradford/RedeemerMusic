from service.service_factory import get_service_factory
ds = get_service_factory().get_drive_service()

songList = [
        {
            "chords": "https://docs.google.com/document/d/1vhY8DxYbViWgIY48WSNJNINZo36L_mmUBLE87CZAYak/edit?usp=sharing",
            "id": 0,
            "lyrics": "https://drive.google.com/file/d/1bQbSIrJXTbG9UzXPum3k-T8lW-aUQ9RL/view?usp=sharing",
            "name": "To God Be The Glory"
        }
    ]

for song in songList:
    name = song['name']
    file_name = name + " (slides).txt"
    ds.upload_slide_file(file_name)
    #f = open(file_name, "r").read()
    #print f
