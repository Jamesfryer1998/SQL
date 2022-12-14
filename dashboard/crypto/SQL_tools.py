import psycopg2
import datetime

class SQLTools:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.connect_string = f'host={host} dbname=postgres user={user} password={password}'
        self.conn = psycopg2.connect(self.connect_string)
        self.time = datetime.datetime.now()
        self.tables = None

    def check_tables(self):
        # MAYBE PUT THIS IN __INIT__
        with self.conn:
            with self.conn.cursor() as cur:
                fetch_sql = '''SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
                '''
                cur.execute(fetch_sql)
                tables = cur.fetchall()
                self.tables = tables
                cur.close()
                
    def delete_rows(self, number_rows):
        return

    def delete_select(self, select):
        print(f'Deleting {len(select)}...')
        with self.conn:
            with self.conn.cursor() as cur:
                for table in select:
                    query = f'''DROP TABLE {table}
                    '''
                    try:
                        cur.execute(query)
                        print(f'Deleted {table}')
        
                    except (Exception, psycopg2.errors.UndefinedTable) as error:
                        print(f'    {table} does not exist.')

    def delete_all(self):
        print('Deleting all...')
        with self.conn:
            with self.conn.cursor() as cur:
                for table in self.tables:
                    query = f'''DROP TABLE {table[0]}
                    '''
                    cur.execute(query)
                    print(f'Deleted {table[0]}')
                cur.close()

# SQL = SQL_tools('localhost', 'postgres', 'mysecretpassword')
# SQL.check_tables()
# SQL.delete_all()
# SQL.delete_select(['eth'])