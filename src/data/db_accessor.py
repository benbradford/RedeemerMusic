import os

import sqlite3

db_dir = os.path.join(os.path.dirname(__file__), './db/')


class DbAccessor:
    class _DbAccess:
        def __init__(self):
            self._con = sqlite3.connect(db_dir + 'redeemer.db', isolation_level=None)

        def __enter__(self):
            return self._con.cursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                print(exc_type)
            if exc_val:
                print(exc_val)
            if exc_tb:
                print(exc_tb)
            if self._con:
                self._con.close()

    def __init__(self):
        self._access = DbAccessor._DbAccess

    def db_access(self):
        return self._access()
