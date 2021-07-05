from db_access import DbAccess, exec_sql_file

def init_db():
    with DbAccess() as cur:
        exec_sql_file(cur, 'song_init_table.sql')
        exec_sql_file(cur, 'service_init_table.sql')
        exec_sql_file(cur, 'user_init.sql')
