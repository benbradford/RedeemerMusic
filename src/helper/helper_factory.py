from helper.powerpoint_creator import PowerpointCreator
from helper.songs_retriever import SongsRetriever
from helper.email_creator import EmailCreator

class HelperFactory:

    def __init__(self, service_factory):
        self._initialised = True
        self._powerpoint_creator = PowerpointCreator(service_factory.get_drive_service())
        self._songs_retriever = SongsRetriever(service_factory.get_drive_service())
        self._email_creator = EmailCreator(self._songs_retriever)

    def get_powerpoint_creator(self):
        return self._powerpoint_creator

    def get_songs_retriever(self):
        return self._songs_retriever

    def get_email_creator(self):
        return self._email_creator

helper_factory = None

def init_helper_factory(service_factory):
    global helper_factory
    if helper_factory is None:
        helper_factory = HelperFactory(service_factory)

def get_helper_factory():
    return helper_factory
