from data_proxy import DataProxy

def service_id_sorter(service):
    string_value = service['id']
    int_value = int(string_value)
    return int_value

class ServiceDao(DataProxy):

    def __init__(self, sheets_client):
        DataProxy.__init__(self, "ser")
        self._sheets_client = sheets_client

    def get_all_services(self):
        services = sorted(self.get_all_keys())
        res = []
        for s in services:
            res.append(self.get(s))
        return sorted(res, key=service_id_sorter, reverse=True)

    def _get_remote_data(self, data_key):
        return self._sheets_client.get_service(data_key)

    def _get_all_remote_data(self):
        return self._sheets_client.get_services()

    def _update_remote_data(self, data, update_data):
        self._sheets_client.update_service(update_data)
        return data

    def _set_remote_data(self, data):
        self._sheets_client.add_service(data)
        return data

    def _get_data_key(self, data):
        return str(data['id'])
