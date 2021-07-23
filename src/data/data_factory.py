from service_dao import ServiceDao
from songs_dao import SongsDao
from user_dao import UserDao


class DataFactory:
    def __init__(self, drive_client, sheets_client):
        self._service_dao = ServiceDao(sheets_client)
        self._songs_dao = SongsDao(sheets_client, drive_client)
        self._user_dao = UserDao()

    def get_service_dao(self):
        return self._service_dao

    def get_songs_dao(self):
        return self._songs_dao

    def get_user_dao(self):
        return self._user_dao


data_factory = None


def init_data_factory(drive_client, sheets_client):
    global data_factory
    if data_factory is None:
        data_factory = DataFactory(drive_client, sheets_client)


def get_data_factory():
    return data_factory
