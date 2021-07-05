from data_common import cache_dir
from db_access import DbAccess

class UserDao:

    def __init__(self):
        pass

    def get(self, user_id):
        with DbAccess() as cur:
            users = cur.execute('SELECT id FROM user').fetchone()
        if not user:
            return None
        user = {}
        user['id'] = user[0]
        user['name'] = user[1]
        user['email'] = user[2]
        user['pic'] = user[3]

        return user

    def set(self, user):
        with DbAccess() as cur:
            cur.execute(
                "INSERT INTO user (id, name, email, profile_pic)"
                " VALUES (?, ?, ?, ?)",
                (user['id'], user['name'], user['email'], user['pic']),
            )
