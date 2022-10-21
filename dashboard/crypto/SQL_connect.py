import psycopg2
import psycopg2.extras as extras
from yfinance_download import *
import json

class SQLConnect:
    def __init__(self, ticker, host, user, password):
        self.ticker = ticker
        self.connect_string = f'host={host} dbname=postgres user={user} password={password}'
        self.conn = psycopg2.connect(self.connect_string)
        self.time = datetime.datetime.now()
        self.tables = None
        download = downloadData('/Users/james/Projects/SQL/Cache')
        download.download_save_data(ticker, 'ytd')
        download.remove_files()
        self.download = download

    def create_table(self):
        query = f'''
        CREATE TABLE {self.ticker} (
            id SERIAL PRIMARY KEY,
            time DATE,
            open FLOAT(4),
            high FLOAT(4),
            low FLOAT(4),
            close FLOAT(4),
            volume FLOAT(4)
        );
        '''
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(query)
                    self.conn.commit()
                    print('SQL: Query Successfully Excecuted.')
                    print(f'    Table {self.ticker} created')
                except psycopg2.errors.DuplicateTable as err:
                    print(f'SQL: {err}')

    def execute_values(self):
        """
        Using psycopg2.extras.execute_values() to insert df to database
        """
        df = self.download.load_data()
        tuples = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns))
        query  = f'''INSERT INTO {self.ticker} ({cols})
        VALUES %s
        '''
        with self.conn:
            with self.conn.cursor() as cur:
                fetch_sql = f'''
                SELECT COUNT(*)
                FROM {self.ticker}
                '''
                cur.execute(fetch_sql)
                table_len = cur.fetchone()[0]

                if table_len >= len(df):
                    print('     Table at sufficient count.')
                    pass
                elif table_len == 0:
                    try:
                        extras.execute_values(cur, query, tuples, page_size=len(df))
                        self.conn.commit()
                    except (Exception, psycopg2.DatabaseError) as error:
                        print("Error: %s" % error)
                        self.conn.rollback()
                        cur.close()
                        return None
                    print(f"    Values populated to {self.ticker}")
                    cur.close()

    def check_tables(self):
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

        tables = []
        for i in range(0, len(self.tables)):
            tables.append(self.tables[i][0].upper())

        with open('/Users/james/Projects/SQL/dashboard/crypto/crypto_list.json', 'r+') as f:
            data = json.load(f)
            print(len(data['crypto']))
            print(len(tables))
            if len(data['crypto']) != len(tables):
                difference = [x for x in tables if x not in set(data['crypto'])]
                new_data = data['crypto'] + difference
                new_dict = {"crypto":sorted(new_data)}
                # json.dump(new_dict, f)
                print(new_dict)
                with open('/Users/james/Projects/SQL/dashboard/crypto/crypto_list.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(new_dict, indent=2))
            else:
                print('JSON: Cryptos match')

    def update_table(self):
        tables = self.tables
        # Search for lower case ticker in query 
        reg_search = re.search(self.ticker.lower(), str(tables))
        if reg_search != None:
            # get the current date
            with self.conn:
                with self.conn.cursor() as cur:
                    query = f'''SELECT time
                    FROM {self.ticker}
                    limit 1
                    '''
                    cur.execute(query)
                    date = str(cur.fetchall()[0][0])
                    
                    # Defining df dates
                    df = self.download.load_data()
                    start = df[df['time'] == date].index[0]
                    end = df[df['time'] == str(self.time.date())].index[0]
                    df_slice = df.iloc[end:start]

                    if len(df_slice) >= 1:
                        # Extracting info from df
                        tuples = [tuple(x) for x in df_slice.to_numpy()]
                        cols = ','.join(list(df_slice.columns))

                        # SQL query and connection
                        query  = f'''INSERT INTO {self.ticker} ({cols})
                        VALUES %s
                        '''
                        try:
                            extras.execute_values(cur, query, tuples, page_size=len(df))
                            self.conn.commit()
                            print(f'     {self.ticker} successfully updated.')
                        except (Exception, psycopg2.DatabaseError) as error:
                            print("Error: %s" % error)
                            self.conn.rollback()
                            cur.close()
                            return None
                    else:
                        return 0

# SQL = SQLConnect('LINK', 'localhost', 'postgres', 'mysecretpassword')
# # SQL.create_table()
# # SQL.execute_values()
# SQL.check_tables()
# # Comment this out if creating table for first time (maybe wont matter)
# SQL.update_table()