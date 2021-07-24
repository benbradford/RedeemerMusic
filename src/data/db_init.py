from db_accessor import DbAccessor, db_dir


def exec_sql_file(cur, file_name):
    cur.execute(open(db_dir + file_name, "r").read()).fetchall()


def init_db():
    accessor = DbAccessor()
    with accessor.db_access() as cur:
        exec_sql_file(cur, 'song_init_table.sql')
        exec_sql_file(cur, 'service_init_table.sql')
        exec_sql_file(cur, 'user_init.sql')
