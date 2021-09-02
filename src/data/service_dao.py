from db_accessor import DbAccessor


class ServiceDao(DbAccessor):

    def __init__(self, sheets_client):
        DbAccessor.__init__(self)
        self._sheets_client = sheets_client

    def get_all_services(self):
        return self._db_get_services()

    def get(self, service_id):
        return self._db_get_service(service_id)

    def sync(self, force=True):
        if force:
            with self.db_access() as cur:
                cur.execute("delete from service")
            services = self._sheets_client.get_services
            print("syncing services: ")
            self._db_add_services(services)

    def update(self, service):
        self._sheets_client.update_service(service)
        self._db_update_service(service)
        return service

    def set(self, service):
        self._sheets_client.add_service(service)
        self._db_add_service(service)
        return service

    def _db_update_service(self, service):
        with self.db_access() as cur:
            cur.execute("""
                update service set(id, date, message, lead, band1, band2, band3, band4, 
                song1, song2, song3, song4, song5, song6, email_status, slides_email_status)=
                ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                where(id = ?)
                """, (service['id'],
                      service['date'],
                      service.get('message'),
                      service.get('lead', ''),
                      service.get('band1', ''),
                      service.get('band2', ''),
                      service.get('band3', ''),
                      service.get('band4', ''),
                      service.get('song1', ''),
                      service.get('song2', ''),
                      service.get('song3', ''),
                      service.get('song4', ''),
                      service.get('song5', ''),
                      service.get('song6', ''),
                      service.get('email_status', 'not sent test'),
                      service.get('slides_email_status', 'not sent test'),
                      service['id']))

    def _db_add_services(self, services):
        with self.db_access() as cur:
            for service in services:
                values_to_add = (service['id'],
                                 service['date'],
                                 service.get('message', ''),
                                 service.get('lead', ''),
                                 service.get('band1', ''),
                                 service.get('band2', ''),
                                 service.get('band3', ''),
                                 service.get('band4', ''),
                                 service.get('song1', ''),
                                 service.get('song2', ''),
                                 service.get('song3', ''),
                                 service.get('song4', ''),
                                 service.get('song5', ''),
                                 service.get('song6', ''),
                                 service.get('email_status', 'not sent test'),
                                 service.get('slides_email_status', 'not sent test'))

                cur.execute("""
                insert into service(id, date, message, lead, band1, band2, band3, band4, 
                song1, song2, song3, song4, song5, song6, email_status, slides_email_status)
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, values_to_add)

    def _db_add_service(self, service):
        self._db_add_services([service])

    def _db_get_service_dates(self):
        with self.db_access() as cur:
            services = cur.execute('SELECT id FROM service ORDER BY id desc').fetchall()
        res = []
        if services:
            for service in services:
                res.append(service[0])
        return res

    def _db_get_services(self):
        with self.db_access() as cur:
            services = cur.execute('SELECT * FROM service ORDER BY id desc').fetchall()
        res = []
        for service in services:
            r = ServiceDao._db_to_service(service)
            res.append(r)
        return res

    def _db_get_service(self, service_id):
        with self.db_access() as cur:
            res = cur.execute('SELECT * FROM service where id=:service_id', {'service_id': service_id}).fetchall()
        if not res:
            return None
        return ServiceDao._db_to_service(res[0])

    @staticmethod
    def service_id_sorter(service):
        string_value = service['id']
        int_value = int(string_value)
        return int_value

    @staticmethod
    def _db_to_service(service):
        r = {'id': service[0], 'date': service[1], 'message': service[2], 'lead': service[3], 'band1': service[4],
             'band2': service[5], 'band3': service[6], 'band4': service[7], 'song1': service[8], 'song2': service[9],
             'song3': service[10], 'song4': service[11], 'song5': service[12], 'song6': service[13],
             'email_status': service[14], 'slides_email_status': service[15]}
        return r
