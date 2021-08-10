from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user):
        if user is None:
            return
        self.id = user['id']
        self.name = user['name']
        self.email = user['email']
        self.profile_pic = user['pic']
        self.scope = user['scope']

    def can_edit(self):
        return self.scope == 'rdm/all' or self.scope == 'rdm/captain' or self.scope == 'rdm/sergeant'

    def can_email(self):
        return self.scope == 'rdm/all' or self.scope == 'rdm/captain'

    def is_admin(self):
        return self.scope == 'rdm/all'

    @staticmethod
    def get_default_scope():
        return 'rdm/private'


    @staticmethod
    def default():
        return User(None)
