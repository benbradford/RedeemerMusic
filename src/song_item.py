class SongItem:
    def __init__(self, item):
        self._name = self.get_or_default(item, 'name')
        self._id = self.get_or_default(item, 'id')
        self._key = self.get_or_default(item, 'key', 'default')
        self._lyrics = self.get_or_default(item, 'lyrics')
        self._chords = self.get_or_default(item, 'chords')
        self._lead = self.get_or_default(item, 'lead')

    def expand_html(self):
        return '<li>{} - {}{}{}</li>'.format(self._name, \
        self.hyperlink('lyrics', self._lyrics), \
        self.hyperlink('chords', self._chords), \
        self.hyperlink('lead', self._lead))

    def hyperlink(self, name, prop):
        if prop is not None:
            return ' <a href="{}">[{}]</a> '.format(prop, name)
        return ''

    def get_or_default(self, item, key, fallback = None):
        try:
            return item[key]
        except:
            if fallback is None:
                raise Exception('cannot fallback for key ' + key)
            return fallback
