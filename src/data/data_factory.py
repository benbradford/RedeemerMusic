from remote_cache_manager import RemoteCacheManager
from local_cache_manager import LocalCacheManager
from data_retriever import DataRetriever
from cache import Cache

class DataFactory:
    def __init__(self, drive_service, sheets_service, slides_helper):
        cache = Cache()
        self._retriever = DataRetriever(cache)
        self._lcm = LocalCacheManager(cache)
        self._rcm = RemoteCacheManager(drive_service, sheets_service, slides_helper, self._lcm)

    def get_local_cache_manager(self):
        return self._lcm

    def get_remote_cache_manager(self):
        return self._rcm

    def get_data_retriever(self):
        return self._retriever

data_factory = None

def init_data_factory(drive_service, sheets_service, slides_helper):
    global data_factory
    if data_factory is None:
        data_factory = DataFactory(drive_service, sheets_service, slides_helper)

def get_data_factory():
    return data_factory
