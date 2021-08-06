import os.path
from db_accessor import DbAccessor, db_dir


def exec_sql_file(cur, file_name):
    cur.execute(open(db_dir + file_name, "r").read()).fetchall()


def exec_custom(cur, dir_name):
    i = 1
    while True:
        file_name = dir_name + '/' + str(i) + '.sql'
        if os.path.isfile(db_dir + file_name):
            exec_sql_file(cur, file_name)
            i = i + 1
        else:
            return


def init_db():
    accessor = DbAccessor()
    with accessor.db_access() as cur:
        exec_custom(cur, 'custom_before')

        exec_sql_file(cur, 'song_init_table.sql')
        exec_sql_file(cur, 'service_init_table.sql')
        exec_sql_file(cur, 'user_init.sql')
        exec_sql_file(cur, 'recipient_init.sql')
        exec_sql_file(cur, 'members_init.sql')
        exec_custom(cur, 'custom_after')


if __name__ == "__main__":
    init_db()