class Member:
    def __init__(self, node):
        self._name = node['name']
        self._instrument = node['instrument']
        self._id = node['id']

    def expand_html(self, lead):
        lead_str = ''
        if lead == self._name:
            lead_str = ' (Lead)'
        return '<li>{} - {}{}</li>'.format(self._instrument, self._name, lead_str)
