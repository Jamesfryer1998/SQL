import psycopg2
import psycopg2.extras as extras
from yfinance_download import *

class SQLConnect:
    def __init__(self, ticker, host, user, password):
        self.ticker = ticker
        self.connect_string = f'host={host} dbname=postgres user={user} password={password}'
        self.conn = psycopg2.connect(self.connect_string)
        download = downloadData('Cache')
        download.download_save_data(ticker, 'ytd')
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
                    print(f'    Query Successfully Excecuted.')
                except psycopg2.errors.DuplicateTable as err:
                    print(f'    SQL: {err}')

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
                    print('Table at sufficient count.')
                    pass
                elif table_len == 0:
                    try:
                        extras.execute_values(cur, query, tuples)
                        self.conn.commit()
                    except (Exception, psycopg2.DatabaseError) as error:
                        print("Error: %s" % error)
                        self.conn.rollback()
                        cur.close()
                        return None
                    print(f"    Values populated to {self.ticker}")
                    cur.close()

#test

SQL = SQLConnect('ETH', 'localhost', 'postgres', 'mysecretpassword')
SQL.create_table()
SQL.execute_values()

# # test
# connect_string = f'host=localhost dbname=postgres user=postgres password=mysecretpassword'
# conn = psycopg2.connect(connect_string)
# cur = conn.cursor()



# ticker = 'ETH'
# sql = f'''
# COPY ETH FROM '/Users/james/Projects/SQL/Cache/ETH-2022-10-06.csv' DELIMITER ',' CSV HEADER;
# '''

# try:
#     cur.execute(sql)
#     conn.commit()
# except psycopg2.errors.DuplicateTable as error:
#     print(f'SKIP: Duplicated {ticker} TABLE')

# # Close communications with database
# cur.close()
# conn.close()

