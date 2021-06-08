from helper.slides_helper import SlidesHelper
from helper.songs_retriever import SongsRetriever

class HelperFactory:

    def __init__(self, service_factory):
        self._initialised = True
        self._slides_helper = SlidesHelper(service_factory.get_drive_service())
        self._songs_retriever = SongsRetriever(service_factory.get_drive_service())

    def get_slides_helper(self):
        return self._slides_helper

    def get_songs_retriever(self):
        return self._songs_retriever

helper_factory = None

def init_helper_factory(service_factory):
    global helper_factory
    if helper_factory is None:
        helper_factory = HelperFactory(service_factory)

def get_helper_factory():
    return helper_factory
