import os
import time
import threading
import datetime
# from data_utilities import open_json
from SQL_connect import SQLConnect
from __init__ import open_json

def worker(crypto, crypto_cache, postgresSQL):
    SQL = SQLConnect(crypto, crypto_cache, postgresSQL['host'], postgresSQL['user'], postgresSQL['password'])
    SQL.load_data()

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
    _, _, files = next(os.walk("/Users/james/Projects/SQL/Cache/crypto_data"))
    file_count = len(files)
    crypto_list = open_json('/Users/james/Projects/SQL/dashboard/crypto/crypto_list.json')

    if file_count != len(crypto_list['crypto']):
        main()
    else:
        time.sleep(0.5)
        print('All cryptos successfully processed.')