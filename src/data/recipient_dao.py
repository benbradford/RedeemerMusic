from db_accessor import DbAccessor


class RecipientDao(DbAccessor):
    TEST_EMAIL_RECIPIENT_FLAG_INDEX = 0
    PPT_EMAIL_RECIPIENT_FLAG_INDEX = 1
    SERVICE_EMAIL_RECIPIENT_FLAG_INDEX = 2

    def __init__(self):
        DbAccessor.__init__(self)

    def get_recipients(self):
        with self.db_access() as cur:
            res = cur.execute('SELECT * FROM recipient').fetchall()
        recipients = []
        if res:
            for r in res:
                recipients.append({'email': r[0], 'name': r[1], 'register': r[2]})
        return recipients

    def get_addresses(self):
        recipients = self.get_recipients()
        res = []
        for r in recipients:
            res.append(r['email'])
        return res

    def get_recipient(self, email):
        with self.db_access() as cur:
            res = cur.execute('SELECT * FROM recipient WHERE (email = :user_email)', {'user_email': email}).fetchone()
        return {'email': res[0], 'name': res[1], 'register': res[2]}

    def is_registered_for_test_emails(self, recipient):
        return self._is_registered_for_emails(recipient, RecipientDao.TEST_EMAIL_RECIPIENT_FLAG_INDEX)

    def is_registered_for_ppt_emails(self, recipient):
        return self._is_registered_for_emails(recipient, RecipientDao.PPT_EMAIL_RECIPIENT_FLAG_INDEX)

    def is_registered_for_service_emails(self, recipient):
        return self._is_registered_for_emails(recipient, RecipientDao.SERVICE_EMAIL_RECIPIENT_FLAG_INDEX)

    def get_test_email_recipients(self):
        return self._get_registered_email_recipients(RecipientDao.TEST_EMAIL_RECIPIENT_FLAG_INDEX)

    def get_ppt_email_recipients(self):
        return self._get_registered_email_recipients(RecipientDao.PPT_EMAIL_RECIPIENT_FLAG_INDEX)

    def get_service_email_recipients(self):
        return self._get_registered_email_recipients(RecipientDao.SERVICE_EMAIL_RECIPIENT_FLAG_INDEX)

    def get_test_email_addresses(self):
        return self._get_email_addresses(RecipientDao.TEST_EMAIL_RECIPIENT_FLAG_INDEX)

    def get_ppt_email_addresses(self):
        return self._get_email_addresses(RecipientDao.PPT_EMAIL_RECIPIENT_FLAG_INDEX)

    def get_service_email_addresses(self):
        return self._get_email_addresses(RecipientDao.SERVICE_EMAIL_RECIPIENT_FLAG_INDEX)

    def set_recipient(self, email, name, test, ppt, service):
        register = RecipientDao._get_register('000', test, ppt, service)
        recipient = {'email': email, 'name': name, 'register': register}
        values_to_add = (email, name, register)
        with self.db_access() as cur:
            cur.execute('INSERT INTO recipient(email, name, register) VALUES(?, ?, ?)', values_to_add)
        return recipient

    def update_recipient(self, email, name, test, ppt, service):
        recipient = self.get_recipient(email)
        register = RecipientDao._get_register(recipient['register'], test, ppt, service)
        recipient['register'] = register
        with self.db_access() as cur:
            cur.execute('UPDATE recipient SET (name, register)=(?, ?) WHERE (email = ?)', (name, register, email))
        return recipient

    def _get_registered_email_recipients(self, flag_index):
        recipients = self.get_recipients()
        res = []
        for r in recipients:
            if self._is_registered_for_emails(r, flag_index):
                res.append(r)
        return res

    def _is_registered_for_emails(self, recipient, flag_index):
        return recipient['register'][flag_index] == '1'

    def _get_email_addresses(self, flag):
        recipients = self._get_registered_email_recipients(flag)
        res = []
        for r in recipients:
            res.append(r['email'])
        return res

    @staticmethod
    def _get_register(old_register, test, ppt, service):
        register = list(old_register)
        if test is not None:
            if test is False:
                register[RecipientDao.TEST_EMAIL_RECIPIENT_FLAG_INDEX] = '0'
            else:
                register[RecipientDao.TEST_EMAIL_RECIPIENT_FLAG_INDEX] = '1'
        if ppt is not None:
            if ppt is False:
                register[RecipientDao.PPT_EMAIL_RECIPIENT_FLAG_INDEX] = '0'
            else:
                register[RecipientDao.PPT_EMAIL_RECIPIENT_FLAG_INDEX] = '1'
        if service is not None:
            if service is False:
                register[RecipientDao.SERVICE_EMAIL_RECIPIENT_FLAG_INDEX] = '0'
            else:
                register[RecipientDao.SERVICE_EMAIL_RECIPIENT_FLAG_INDEX] = '1'
        return "".join(register)
