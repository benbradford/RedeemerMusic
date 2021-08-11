from db_accessor import DbAccessor


class UserDao(DbAccessor):

    def __init__(self):
        DbAccessor.__init__(self)

    def get_all(self):
        with self.db_access() as cur:
            res = cur.execute('select * from user').fetchall()
        if res is None:
            return []
        users = []
        for r in res:
            users.append(UserDao._get_user_from_query_result(r))
        return users

    def get(self, user_id):
        with self.db_access() as cur:
            res = cur.execute('SELECT * FROM user where id=:user_id', {'user_id': user_id}).fetchone()
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

    def update_scope(self, user_id, scope):
        with self.db_access() as cur:
            cur.execute('UPDATE user SET scope=? WHERE id=?', (scope, str(user_id)))

    @staticmethod
    def _get_user_from_query_result(res):
        return {'id': res[0], 'name': res[1], 'email': res[2], 'scope': res[3], 'pic': res[4]}


