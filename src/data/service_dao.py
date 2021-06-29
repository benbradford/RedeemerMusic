from data_proxy import DataProxy

class ServiceDao(DataProxy):

    def __init__(self, sheets_client):
        DataProxy.__init__(self, "ser")
        self._sheets_client = sheets_client

    def _get_remote_data(self, data_key):
        return self._sheets_client.get_service(data_key)

    def _get_all_remote_data(self):
        return self._sheets_client.get_services()

    def _update_remote_data(self, data):
        self._sheets_client.update_service(data)

    def _get_data_key(self, data):
        return str(data['id'])
