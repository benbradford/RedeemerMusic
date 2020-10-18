class Member:
    def __init__(self, node):
        self._name = node['name']
        self._instrument = node['instrument']
        self._id = node['id']

    def expand(self, lead):
        if lead == self._name:
            return self._instrument + '/Lead - ' + self._name
        return self._instrument + ' - ' + self._name

    def expand_html(self, lead):
        if lead == self._name:
            return '<li>' + self._instrument + '/Lead - ' + self._name + '</li>'
        return '<li>' + self._instrument + ' - ' + self._name + '</li>'
