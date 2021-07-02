from database import db

class DataProxy:

    def __init__(self, prefix):
        pass

    def get(self, data_key):
        return self._get_remote_data(data_key)

    def sync(self, force=False):
        if force:
            elements = self._get_all_remote_data()

    def get_all_keys(self):
        pass

    def get_all(self):
        pass

    def update(self, element):
        self.update_with(element, element)

    def set(self, set_data):
        self._set_remote_data(set_data)

    def _get_remote_data(self, id):
        pass

    def _get_all_remote_data(self):
        pass

    def _set_remote_data(self, data):
        pass

    def _update_remote_data(self, data, update_data):
        pass


dp = DataProxy("")
db.set({})
