import json
import base64
from flask import request, jsonify, send_file, render_template

from api_common import app, extract_required_param
from data.data_factory import get_data_factory

data_retriever = get_data_factory().get_data_retriever()
remote_data_manager = get_data_factory().get_remote_data_manager()
songs_dao = get_data_factory().get_songs_dao()

def get_song_from_params(name, component, files):
    if component in request.files:
        uploaded_file = request.files[component]
        if uploaded_file.filename != '':
            type = uploaded_file.filename.split('.')[1]
            file_name = name + ' (' + component + ')'
            if '(slides)' in file_name:
                file_name = file_name + '.txt'
            out_path = 'bin/' + file_name
            uploaded_file.save(out_path)
            files.append({'path': out_path, 'type': type})

def get_song_files_from_params(song_name):
    files = []
    get_song_from_params(song_name, 'lyrics', files)
    get_song_from_params(song_name, 'lead', files)
    get_song_from_params(song_name, 'chords', files)
    get_song_from_params(song_name, 'slides', files)
    return files

def _get_slides(song):
    print song['file_ids']
    if 'slides' not in song['file_ids']:
        return None
    lines = data_retriever.get_slide(song['name']).decode('utf-8').split('\n')
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
    song = data_retriever.get_song(song_name)
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
    song = data_retriever.get_song(song_name)
    slides = data_retriever.get_slide(song_name)
    return render_template('slides_edit.html', song=song, slides=slides)

@app.route('/update_slides', methods=['GET'])
def update_slides_api():
    lyrics = extract_required_param('lyrics').replace("%20", " ").replace("%0D%0A", '\n')
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    remote_data_manager.update_slide_for_song(song, lyrics)
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
    if data_retriever.get_song(song_name) is not None:
        return "Error, " + song_name + " already exists"
    files = get_song_files_from_params(song_name)
    remote_data_manager.add_song(song_name, files, ccli)
    names = data_retriever.get_song_names()
    return render_template('songs.html')

@app.route('/update_song_page', methods=['GET'])
def update_song_page_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    return render_template('song_edit.html', song=song, ccli='')

@app.route('/update_song', methods=['POST'])
def update_song_api():
    song_name = request.form.get('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    old_song_name = request.form.get('previous').replace("%20", " ")
    if old_song_name != song_name:
        raise ("Currently unable to rename songs")
    ccli = ""
    if 'ccli' in request.form:
        ccli = request.form.get('ccli')
    files = get_song_files_from_params(song_name)
    song = remote_data_manager.update_song(old_song_name, song_name, song['file_ids'], files, ccli)
    components = {}
    _update_component_file_ids(song, 'lyrics', components)
    _update_component_file_ids(song, 'chords', components)
    _update_component_file_ids(song, 'lead', components)
    return render_template('song.html',
            song_name=song_name, # TODO pass in song instead
            components=components,
            slides=_get_slides(song)
    )
