import os
import time
import threading
import datetime
from data_utilities import open_json
from SQL_connect import SQLConnect
import psycopg2

def worker(crypto, crypto_cache, postgres):
    postgresSQL = postgres
    
    # print(f'\n----------------{crypto}----------------\n')
    SQL = SQLConnect(crypto, crypto_cache, postgresSQL['host'], postgresSQL['user'], postgresSQL['password'])
    SQL.create_table()
    SQL.check_tables()
    SQL.validate_data()
    try:
        SQL.execute_values()
    except (Exception, psycopg2.errors.UndefinedTable) as error:
        SQL.create_table()
        SQL.execute_values()
    SQL.update_table()

    # print(f'{crypto.upper()} successfully processed.')

def main():
    t1 = datetime.datetime.now()  

    crypto_cache = '/Users/james/Projects/SQL/Cache/crypto_data'
    crypto_list = open_json('/Users/james/Projects/SQL/dashboard/crypto/crypto_list.json')
    postgresSQL = open_json('/Users/james/Projects/SQL/dashboard/crypto/postgres_login.json')
    num = len(crypto_list['crypto'])

    for crypto in crypto_list['crypto']:
        t = threading.Thread(target=worker, args=[crypto, crypto_cache, postgresSQL])
        t.start()

    print('------------------------------------')
    t2 = datetime.datetime.now()
    print(f'Programme excected in {t2 - t1} - {num} cryptos processed.')

if __name__ == '__main__':
    main()
    time.sleep(1)
    _, _, files = next(os.walk("/Users/james/Projects/SQL/Cache/crypto_data"))
    file_count = len(files)
    crypto_list = open_json('/Users/james/Projects/SQL/dashboard/crypto/crypto_list.json')

    if file_count != len(crypto_list['crypto']):
        main()
    else:
        print('All cryptos successfully processed.')