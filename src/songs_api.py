import json
import base64
from flask import request, jsonify, send_file, render_template

from api_common import app, extract_required_param
from data.data_factory import get_data_factory

songs_dao = get_data_factory().get_songs_dao()

def get_song_from_params(name, component, new_song_data):
    if component in request.files:
        uploaded_file = request.files[component]
        if uploaded_file.filename != '':
            type = uploaded_file.filename.split('.')[1]
            file_name = name + ' (' + component + ')'
            if '(slides)' in file_name:
                file_name = file_name + '.txt'
            out_path = 'bin/' + file_name # TODO relative path
            uploaded_file.save(out_path)
            new_song_data[component] = {'path': out_path, 'type': type}

def get_song_file_data_from_params(song_name):
    new_song_data = {}
    new_song_data['name'] = song_name
    get_song_from_params(song_name, 'lyrics', new_song_data)
    get_song_from_params(song_name, 'lead', new_song_data)
    get_song_from_params(song_name, 'chords', new_song_data)
    get_song_from_params(song_name, 'slides', new_song_data)
    return new_song_data

def _get_slides(song):
    lines = song['slides'].decode('utf-8').split('\n')
    pages = []
    page = []
    for l in lines:
        if not any(c.isalpha() for c in l):
            if len(page) > 0:
                pages.append(page)
                page = []
        else:
            page.append(l)
    if len(page) > 0:
        pages.append(page)
    return pages

def _update_component_file_ids(song, component, components):
    if component in song['file_ids']:
        components[component] = song['file_ids'][component]
    else:
        components[component] = None

@app.route('/songs', methods=['GET'])
def songs_api():
    names = sorted(songs_dao.get_song_names())
    return render_template('songs.html', song_names=names)

@app.route('/song', methods=['GET'])
def song_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = songs_dao.get(song_name)
    components = {}
    _update_component_file_ids(song, 'lyrics', components)
    _update_component_file_ids(song, 'chords', components)
    _update_component_file_ids(song, 'lead', components)
    return render_template('song.html',
        song_name=song_name,
        components=components,
        slides=_get_slides(song)
    )

@app.route('/edit_slides', methods=['GET'])
def edit_slides_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = songs_dao.get(song_name)
    return render_template('slides_edit.html', song=song, slides=song['slides']) # todo no need to pass in 2 params

@app.route('/update_slides', methods=['GET'])
def update_slides_api():
    lyrics = extract_required_param('lyrics').replace("%20", " ").replace("%0D%0A", '\n')
    song_name = extract_required_param('name').replace("%20", " ")
    song = songs_dao.get(song_name)
    update = {}
    update['name'] = song['name']
    update['file_ids'] = {}
    update['slides'] = lyrics
    songs_dao.update_with(song, update)
    components = {}
    _update_component_file_ids(song, 'lyrics', components)
    _update_component_file_ids(song, 'chords', components)
    _update_component_file_ids(song, 'lead', components)
    return render_template('song.html',
            song_name=song_name,
            components=components,
            slides=_get_slides(song)
        )

@app.route('/add_song_page', methods=['GET'])
def add_song_page_api():
    return render_template('song_add.html')

@app.route('/add_song', methods=['POST'])
def add_song_api():
    song_name = request.form.get('name').replace("%20", " ")
    ccli = ""
    if 'ccli' in request.form:
        ccli = request.form.get('ccli')
    print ("adding song " + song_name)

    new_song_data = get_song_file_data_from_params(song_name)

    songs_dao.set(new_song_data)
    names = sorted(songs_dao.get_song_names())
    return render_template('songs.html')

@app.route('/update_song_page', methods=['GET'])
def update_song_page_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = songs_dao.get(song_name)
    return render_template('song_edit.html', song=song, ccli='')

@app.route('/update_song', methods=['POST'])
def update_song_api():
    song_name = request.form.get('name').replace("%20", " ")
    song = songs_dao.get(song_name)
    old_song_name = request.form.get('previous').replace("%20", " ")
    if old_song_name != song_name:
        raise ("Currently unable to rename songs")
    ccli = ""
    if 'ccli' in request.form:
        ccli = request.form.get('ccli')
    update_data = get_song_file_data_from_params(song_name)
    song = songs_dao.update_with(song, update_data)
    components = {}
    _update_component_file_ids(song, 'lyrics', components) # todo, is this needed?
    _update_component_file_ids(song, 'chords', components)
    _update_component_file_ids(song, 'lead', components)
    return render_template('song.html',
            song_name=song_name, # TODO pass in song instead
            components=components,
            slides=_get_slides(song)
    )
