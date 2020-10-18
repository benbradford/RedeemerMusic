class SongItem:
    def __init__(self, item):
        self._name = self.get_or_default(item, 'name')
        self._id = self.get_or_default(item, 'id')
        self._key = self.get_or_default(item, 'key', 'default')
        self._lyrics = self.get_or_default(item, 'lyrics')
        self._chords = self.get_or_default(item, 'chords')
        self._lead = self.get_or_default(item, 'lead')

    def expand_html(self):
        return '<li>' + self._name + ' - [lyrics] [chords] [lead]' + '</li>'

    def expand(self):
        return self._name

    def get_or_default(self, item, key, fallback = None):
        try:
            return item[key]
        except:
            if fallback is None:
                raise Exception('cannot fallback for key ' + key)
            return fallback
