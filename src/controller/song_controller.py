from flask import render_template
from util import redirect_url, UNAUTHORISED
from controller import Controller


class SongController(Controller):

    def __init__(self, user, log_helper, songs_dao):
        Controller.__init__(self, user, log_helper, 'SongController')
        self._songs_dao = songs_dao

    def show_songs_page(self):
        names = sorted(self._songs_dao.get_song_names())
        return render_template('songs.html', user=self._user, song_names=names)

    def show_song_page(self, song_name):
        song = self._songs_dao.get(song_name)
        components = {}
        SongController._update_component_file_ids(song, 'lyrics', components)
        SongController._update_component_file_ids(song, 'chords', components)
        SongController._update_component_file_ids(song, 'lead', components)
        return render_template('song.html',
                               user=self._user,
                               song_name=song_name,
                               components=components,
                               slides=SongController._get_slides(song)
                               )

    def show_edit_slides_page(self, song_name):
        if not self._user.is_authenticated or not self._user.can_edit():
            self._log_warn("user is not authorised to show edit slides page")
            return UNAUTHORISED
        song = self._songs_dao.get(song_name)
        return render_template('slides_edit.html', user=self._user, song=song,
                               slides=song['slides'])  # todo no need to pass in 2 params

    def update_slides(self, song_name, lyrics):
        if not self._user.is_authenticated or not self._user.can_edit():
            self._log_warn("user is not authorised to update slides")
            return UNAUTHORISED
        file_name = song_name + " (slides).txt"
        file_path = "bin/" + song_name  # TODO fix path
        out_f = open(file_path, "w")
        out_f.write(lyrics)
        out_f.close()
        upload_data = {'file_type': 'txt', 'file_path': file_path, 'file_name': file_name}
        creation_data = {'slides': upload_data}
        self._songs_dao.update(song_name, creation_data)
        self._log_info("slides updated for " + song_name)
        return redirect_url('song_api', name=song_name)

    def show_add_song_page(self):
        if not self._user.is_authenticated or not self._user.can_edit():
            self._log_warn("user is not authorised to show add songs page")
            return UNAUTHORISED
        return render_template('song_add.html', user=self._user)

    def add_song(self, song_name, ccli, files):
        if not self._user.is_authenticated or not self._user.can_edit():
            self._log_warn("user is not authorised to add song")
            return UNAUTHORISED
        song = {'name': song_name, 'file_ids': {}, 'ccli': ccli, 'notes': ''}
        song_creation_data = SongController.get_song_creation_data(song_name, files)
        self._songs_dao.set(song, song_creation_data)
        self._log_info("new song added for " + song_name)
        return redirect_url('songs_api')

    def show_update_song_page(self, song_name):
        if not self._user.is_authenticated or not self._user.can_edit():
            self._log_warn("user is not authorised to view update songs page")
            return UNAUTHORISED
        song = self._songs_dao.get(song_name)
        return render_template('song_edit.html', user=self._user, song=song, ccli='')

    def update_song(self, song_name, old_song_name, files):
        if not self._user.is_authenticated or not self._user.can_edit():
            self._log_warn("user is not authorised to update song")
            return UNAUTHORISED
        if old_song_name != song_name:
            raise Exception("Currently unable to rename songs")
        update_data = SongController.get_song_creation_data(song_name, files)
        self._songs_dao.update(song_name, update_data)
        self._log_info("song updated for " + song_name)
        return redirect_url('song_api', user=self._user, name=song_name)

    @staticmethod
    def get_song_creation_data(song_name, files):
        creation_data = {}
        for component in ['lyrics', 'chords', 'lead', 'slides']:
            if component in files:
                uploaded_file = files[component]
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

    @staticmethod
    def _update_component_file_ids(song, component, components):
        if component in song['file_ids']:
            components[component] = song['file_ids'][component]
        else:
            components[component] = None

    @staticmethod
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
