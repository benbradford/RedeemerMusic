from db_accessor import DbAccessor


class BandDao(DbAccessor):
    def __init__(self, recipient_dao):
        DbAccessor.__init__(self)
        self._recipient_dao = recipient_dao

    def get_member_list(self):
        members = []
        with self.db_access() as cur:
            res = cur.execute('SELECT * FROM member').fetchall()
            for r in res:
                rec = self._recipient_dao.get_recipient(r[0])
                members.append({'name': rec['name'], 'instrument': r[1]})
        members.sort(key=lambda x: x['name'])
        instruments = []
        for m in members:
            instruments.append(m['name'] + ' - ' + m['instrument'])
        return instruments
