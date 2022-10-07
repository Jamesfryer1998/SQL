import psycopg2

class SQLConnect:
    def __init__(self, host, user, password):
        self.connect_string = f'host={host} dbname=postgres user={user} password={password}'
        self.conn = psycopg2.connect(self.connect_string)

    def create_table(self, ticker):
        query = f'''
        CREATE TABLE {ticker} (
            id SERIAL PRIMARY KEY,
            date DATE,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume FLOAT
        );
        '''
        cur = self.conn.cursor()

        try:
            cur.execute(query)
            self.conn.commit()
            print(f'    Query Successfully Excecuted.')
        except psycopg2.errors.DuplicateTable as err:
            print(f'    SKIPPING: {err}')

        cur.close()
        self.conn.close()

    def populate_table(self, ticker):
        query = f'''INSERT INTO {ticker}
        
        '''

        cur = self.conn.cursor()

        try:
            cur.execute(query)
            self.conn.commit()
            print(f'    Query Successfully Excecuted.')
        except psycopg2.errors.DuplicateTable as err:
            print(f'    SKIPPING: {err}')

SQL = SQLConnect('localhost', 'postgres', 'mysecretpassword')
SQL.create_table('ETH')

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

