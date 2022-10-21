from SQL_connect import *
import json
import time

def open_json(path):
    with open(path) as f:
        data = json.load(f)
    return data['crypto']

def main():
    t1 = datetime.datetime.now()
    cryptos = open_json('/Users/james/Projects/SQL/dashboard/crypto/crypto_list.json')

    for crypto in cryptos:
        SQL = SQLConnect(crypto, 'localhost', 'postgres', 'mysecretpassword')
        SQL.create_table()
        SQL.execute_values()
        SQL.check_tables()
        SQL.update_table()

    t2 = datetime.datetime.now()
    print(f'Programme excected in {t2 - t1}')

main()