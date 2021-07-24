from db_accessor import DbAccessor


class UserDao(DbAccessor):

    def __init__(self):
        DbAccessor.__init__(self)

    def get(self, user_id):
        with self.db_access() as cur:
            users = cur.execute('SELECT id FROM user where name=:user_name', {'user_name': user_id}).fetchone()
        if not users:
            return None
        user = {}
        user['id'] = user[0]
        user['name'] = user[1]
        user['email'] = user[2]
        user['pic'] = user[3]

        return user

    def set(self, user):
        with self.db_access() as cur:
            cur.execute(
                "INSERT INTO user (id, name, email, profile_pic)"
                " VALUES (?, ?, ?, ?)",
                (user['id'], user['name'], user['email'], user['pic']),
            )
