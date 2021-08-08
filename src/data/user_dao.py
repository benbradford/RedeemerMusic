from db_accessor import DbAccessor


class UserDao(DbAccessor):

    def __init__(self):
        DbAccessor.__init__(self)

    def get_all(self):
        with self.db_access() as cur:
            return cur.execute('select * from user').fetchall()

    def get(self, email):
        with self.db_access() as cur:
            res = cur.execute('SELECT * FROM user where email=:user_email', {'user_email': email}).fetchone()
        if not res:
            return None

        return UserDao._get_user_from_query_result(res)

    def set(self, user):
        with self.db_access() as cur:
            cur.execute(
                "INSERT INTO user (id, name, email, scope, profile_pic)"
                " VALUES (?, ?, ?, ?, ?)",
                (user['id'], user['name'], user['email'], user['scope'], user['pic']),
            )


    @staticmethod
    def _get_user_from_query_result(res):
        return {'id': res[0], 'name': res[1], 'email': res[2], 'scope': res[3], 'pic': res[4]}
