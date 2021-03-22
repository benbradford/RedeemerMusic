import json

songsstring = open('../res/songs.json', "r").read()
old_songs = json.loads(songsstring)['songList']
new_songs = []
i = 0
for song in old_songs:
    if 'name' not in song:
        song['name'] = song['id']


    if 'ppt' in song:
        ppt_filename = '../' + song['ppt']
    else:
        ppt_filename = '../res/ppt/' + song['id'] + '.json'
    ppt_filename = ppt_filename.replace('.txt', '.json')
    print ('loading slides ' + ppt_filename)
    slides_file = open(ppt_filename, "r").read()
    slides = json.loads(slides_file)

    new_slides_filename = '../res/slides/' + song['name'] + '.json'
    with open(new_slides_filename, 'w+') as f:
        json.dump(slides, f)

    song['id'] = i
    i = i + 1
    song.pop('ppt', None)

    new_songs.append(song)

result = {}
result['songList'] = new_songs
with open('../res/new_songs.json', 'w+') as f:
    json.dump(result, f)
