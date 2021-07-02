import json
import ast
from pymemcache.client.base import Client

cache_client = Client('localhost')

class DataProxy:

    def __init__(self, prefix):
        self._cache_client = cache_client
        self._prefix = "rmv11" + prefix

    def get(self, data_key):
        cache_key = self._get_cache_key(data_key)
        res = self._cache_client.get(cache_key)
        if res is None:
            element = self._get_remote_data(data_key)
            self.set(element)
        else:
            print res
            element = ast.literal_eval(res)
        return element

    def sync(self, force=False):
        if force or self._cache_client.get(self._get_cache_key('ALL_DATA_KEYS')) is None:
            elements = self._get_all_remote_data()
            if elements is not None:
                for element in elements:
                    cache_key, data_key = self._get_cache_and_data_key(element)
                    self._cache_client.set(cache_key, json.dumps(element))
                    self._add_data_key(self._get_data_key(element))

    def get_all_keys(self):
        all_data_keys = self._cache_client.get(self._get_cache_key('ALL_DATA_KEYS'))
        if all_data_keys is None:
            return []
        return all_data_keys.split('|')

    def get_all(self):
        all_data_keys = self.get_all_keys()
        all_songs = {}
        for key in all_data_keys:
            all_songs[key.replace('_', ' ')] = self.get(key)
        return all_songs

    def update_with(self, element, update_data):
        cache_key, data_key = self._get_cache_and_data_key(element)
        current = self.get(data_key)
        if current is None:
            raise Exception("Cannot update, element does not exist")
        new_element = self._update_remote_data(element, update_data)
        self._cache_client.set(cache_key, json.dumps(new_element))

    def update(self, element):
        self.update_with(element, element)

    def set(self, set_data):
        element = self._set_remote_data(set_data)
        cache_key, data_key = self._get_cache_and_data_key(element)
        self._cache_client.set(cache_key, json.dumps(element))
        self._add_data_key(data_key)

    def _get_cache_and_data_key(self, element):
        data_key = self._get_data_key(element)
        cache_key = self._get_cache_key(data_key)
        return cache_key, data_key

    def _add_data_key(self, data_key):
        # TODO add sync
        all = self._cache_client.get(self._get_cache_key('ALL_DATA_KEYS'))
        if all is None:
            all = [data_key]
        else:
            all = all.split('|')
            if data_key not in all:
                all.append(data_key)
        self._cache_client.set(self._get_cache_key('ALL_DATA_KEYS'), '|'.join(all))

    def _get_cache_key(self, id):
        return (self._prefix + str(id)).replace(' ', '_')

    def _get_remote_data(self, id):
        pass

    def _get_all_remote_data(self):
        pass

    def _set_remote_data(self, data):
        pass

    def _update_remote_data(self, data, update_data):
        pass

    def _get_data_key(self, data):
        pass
