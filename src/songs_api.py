import json
import base64
from flask import request, jsonify, send_file

from api_common import app, extract_required_param
from view.songs_view import SongsView
from view.song_view import SongView
from view.edit_slides_view import EditSlidesView
from view.add_song_view import AddSongView
from view.update_song_view import UpdateSongView
from data.data_factory import get_data_factory

data_retriever = get_data_factory().get_data_retriever()
remote_data_manager = get_data_factory().get_remote_data_manager()

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
    else:
        print "No " + component + " in song files"

def get_song_files_from_params(song_name):
    files = []
    get_song_from_params(song_name, 'lyrics', files)
    get_song_from_params(song_name, 'lead', files)
    get_song_from_params(song_name, 'chords', files)
    get_song_from_params(song_name, 'slides', files)
    return files

@app.route('/songs', methods=['GET'])
def songs_api():
    names = data_retriever.get_song_names()
    return SongsView().render(names)

@app.route('/song', methods=['GET'])
def song_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    return SongView(data_retriever).render(song)

@app.route('/refresh_slides', methods=['GET'])
def refresh_slides_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    remote_data_manager.sync_slides_for_song(song)
    return SongView(data_retriever).render(song)

@app.route('/edit_slides', methods=['GET'])
def edit_slides_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)
    slides = data_retriever.get_slide(song_name)
    return EditSlidesView().render(song, slides)

@app.route('/update_slides', methods=['GET'])
def update_slides_api():
    lyrics = extract_required_param('lyrics').replace("%20", " ").replace("%0D%0A", '\n')
    song_name = extract_required_param('name').replace("%20", " ")
    song = data_retriever.get_song(song_name)

    remote_data_manager.update_slide_for_song(song, lyrics)
    return SongView(data_retriever).render(song)

@app.route('/add_song_page', methods=['GET'])
def add_song_page_api():
    return AddSongView().render()

@app.route('/add_song', methods=['POST'])
def add_song_api():
    song_name = request.form.get('name').replace("%20", " ")
    ccli = ""
    if 'ccli' in request.form:
        ccli = request.form.get('ccli')
    print "adding song " + song_name
    if data_retriever.get_song(song_name) is not None:
        print "error - song already exists"
        return "Error, " + song_name + " already exists"
    files = get_song_files_from_params(song_name)
    remote_data_manager.add_song(song_name, files, ccli)
    names = data_retriever.get_song_names()
    return SongsView().render(names)

@app.route('/update_song_page', methods=['GET'])
def update_song_page_api():
    song_name = extract_required_param('name').replace("%20", " ")
    return UpdateSongView(song_name, data_retriever).render()

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
    return SongView(data_retriever).render(song)
