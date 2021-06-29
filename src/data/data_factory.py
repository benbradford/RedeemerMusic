from remote_data_manager import RemoteDataManager
from local_cache_manager import LocalCacheManager
from data_retriever import DataRetriever
from cache import Cache
from service_dao import ServiceDao

class DataFactory:
    def __init__(self, drive_client, sheets_client):
        cache = Cache()
        self._retriever = DataRetriever(cache)
        self._lcm = LocalCacheManager(cache)
        self._rcm = RemoteDataManager(drive_client, sheets_client, self._lcm, self._retriever)
        self._service_dao = ServiceDao(sheets_client)

    def get_local_cache_manager(self):
        return self._lcm

    def get_remote_data_manager(self):
        return self._rcm

    def get_data_retriever(self):
        return self._retriever

    def get_service_dao(self):
        return self._service_dao

data_factory = None

def init_data_factory(drive_client, sheets_client):
    global data_factory
    if data_factory is None:
        data_factory = DataFactory(drive_client, sheets_client)

def get_data_factory():
    return data_factory
