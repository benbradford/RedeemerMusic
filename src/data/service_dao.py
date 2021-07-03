from database import db

def service_id_sorter(service):
    string_value = service['id']
    int_value = int(string_value)
    return int_value

class ServiceDao():

    def __init__(self, sheets_client):
        self._sheets_client = sheets_client

    def get_all_services(self):
        return db.get_services()

    def get(self, id):
        return db.get_service(id)

    def sync(self, force=True):
        if force:
            db.drop_services()
            services = self._sheets_client.get_services()
            db.add_services(services)

    def update(self, service):
        self._sheets_client.update_service(service)
        db.update_service(service)
        return service

    def set(self, service):
        self._sheets_client.update_service(update_data)
        db.add_service(service)
        return service
