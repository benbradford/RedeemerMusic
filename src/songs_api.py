from flask import request, render_template, redirect, url_for

from api_common import app, extract_required_param
from data.data_factory import get_data_factory

songs_dao = get_data_factory().get_songs_dao()


def get_song_creation_data(song_name):
    creation_data = {}
    for component in ['lyrics', 'chords', 'lead', 'slides']:
        if component in request.files:
            uploaded_file = request.files[component]
            if uploaded_file.filename != '':
                upload_data = {}
                file_type = uploaded_file.filename.split('.')[1]
                file_name = song_name + ' (' + component + ')'
                if '(slides)' in file_name:
                    file_name = file_name + '.txt'
                file_path = 'bin/' + file_name  # TODO relative path
                uploaded_file.save(file_path)
                file_name = file_path.split('/')[1]
                if component == 'slides':
                    file_name = file_path.split('/')[1]
                upload_data['file_type'] = file_type
                upload_data['file_path'] = file_path
                upload_data['file_name'] = file_name
                creation_data[component] = upload_data
    return creation_data


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
    return render_template('slides_edit.html', song=song, slides=song['slides'])  # todo no need to pass in 2 params


@app.route('/update_slides', methods=['GET'])
def update_slides_api():
    lyrics = extract_required_param('lyrics').replace("%20", " ").replace("%0D%0A", '\n')
    song_name = extract_required_param('name').replace("%20", " ")

    file_name = song_name + " (slides).txt"
    file_path = "bin/" + song_name  # TODO fix path
    out_f = open(file_path, "w")
    out_f.write(lyrics)
    out_f.close()
    upload_data = {'file_type': 'txt', 'file_path': file_path, 'file_name': file_name}
    creation_data = {'slides': upload_data}
    songs_dao.update(song_name, creation_data)

    return redirect(url_for('song_api', name=extract_required_param('name')))


@app.route('/add_song_page', methods=['GET'])
def add_song_page_api():
    return render_template('song_add.html')


@app.route('/add_song', methods=['POST'])
def add_song_api():
    song_name = request.form.get('name').replace("%20", " ")
    ccli = ""
    if 'ccli' in request.form:
        ccli = request.form.get('ccli')
    song = {'name': song_name, 'file_ids': {}, 'ccli': ccli, 'notes': ''}
    song_creation_data = get_song_creation_data(song_name)
    songs_dao.set(song, song_creation_data)
    return redirect(url_for('songs_api'))


@app.route('/update_song_page', methods=['GET'])
def update_song_page_api():
    song_name = extract_required_param('name').replace("%20", " ")
    song = songs_dao.get(song_name)
    return render_template('song_edit.html', song=song, ccli='')


@app.route('/update_song', methods=['POST'])
def update_song_api():
    song_name = request.form.get('name').replace("%20", " ")
    old_song_name = request.form.get('previous').replace("%20", " ")
    if old_song_name != song_name:
        raise Exception("Currently unable to rename songs")
    update_data = get_song_creation_data(song_name)
    songs_dao.update(song_name, update_data)
    return redirect(url_for('song_api', name=request.form.get('name')))
