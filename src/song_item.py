import json

class SongItem:
    def __init__(self, item):
        self._id = self._get_or_default(item, 'id')
        self._name = self._get_or_default(item, 'name', self._id)
        self._key = self._get_or_default(item, 'key', 'default')
        self._lyrics = self._get_or_default(item, 'lyrics')
        self._chords = self._get_or_default(item, 'chords', None)
        self._lead = self._get_or_default(item, 'lead', None)
        self._ppt = self._get_or_default(item, 'ppt', 'res/ppt/{}.txt'.format(self._id))

    def get_ppt_file(self):
        return self._ppt

    def expand_html(self):
        return '<li>{} - {}{}{}</li>'.format(self._name, \
        self._hyperlink('lyrics', self._lyrics), \
        self._hyperlink('chords', self._chords), \
        self._hyperlink('lead', self._lead))

    def _hyperlink(self, name, prop):
        if prop is not None:
            return ' <a href="{}">[{}]</a> '.format(prop, name)
        return ''

    def _get_or_default(self, item, key, fallback = "error"):
        try:
            return item[key]
        except:
            if fallback is "error":
                raise Exception('cannot use fallback for {} in file {}'.format(key, self._id))
            return fallback
