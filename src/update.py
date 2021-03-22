import json
import os

songsstring = open('../res/songs.json', "r").read()
songs = json.loads(songsstring)
slides = {}
slides['presentations'] = []
for slides_file in os.listdir('../res/slides'):
    file = open('../res/slides/' + slides_file, "r").read()
    print slides_file
    output = json.loads(file)
    id = -1
    for song in songs['songList']:
        print song
        if slides_file == song['name'] + '.json':
            id = song['id']
    output['id'] = id
    slides['presentations'].append(output);

with open('../res/new_slides.json', 'w+') as f:
    json.dump(slides, f, indent=4, sort_keys=True)
