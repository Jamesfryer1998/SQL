import psycopg2

class SQLConnect:
    def __init__(self, ticker, host, user, password):
        self.connect_string = f'host={host} dbname=postgres user={user} password={password}'
        self.ticker = ticker
        self.conn = psycopg2.connect(self.connect_string)

    def create_table(self):
        query = '''
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
        except psycopg2.errors.DuplicateTable as error:
            print(f'SKIP: Duplicated {self.ticker} TABLE')

        cur.close()
        self.conn.close()

# test
# connect_string = f'host=localhost dbname=postgres user=postgres password=mysecretpassword'
# conn = psycopg2.connect(connect_string)
# cur = conn.cursor()

# ticker = 'ETH'
# sql = f'''
# CREATE TABLE {ticker} (
#     id SERIAL PRIMARY KEY,
#     date DATE,
#     open FLOAT,
#     high FLOAT,
#     low FLOAT,
#     close FLOAT,
#     volume FLOAT
# );
# '''

# try:
#     cur.execute(sql)
#     conn.commit()
# except psycopg2.errors.DuplicateTable as error:
#     print(f'SKIP: Duplicated {ticker} TABLE')

# # Close communications with database
# cur.close()
# conn.close()

