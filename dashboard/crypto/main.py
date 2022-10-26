from SQL_connect import SQLConnect
import psycopg2
import datetime
import json

def open_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def main():
    t1 = datetime.datetime.now()
    cryptos = open_json('/Users/james/Projects/SQL/dashboard/crypto/crypto_list.json')
    postgresSQL = open_json('/Users/james/Projects/SQL/dashboard/crypto/postgres_login.json')
    
    for crypto in cryptos['crypto']:
        print(f'\n----------------{crypto}----------------\n')
        SQL = SQLConnect(crypto, postgresSQL['host'], postgresSQL['user'], postgresSQL['password'])
        SQL.create_table()
        SQL.check_tables()
        SQL.validate_data()
        try:
            SQL.execute_values()
        except (Exception, psycopg2.errors.UndefinedTable) as error:
            SQL.create_table()
            SQL.execute_values()
        SQL.update_table()
        
    t2 = datetime.datetime.now()
    print('------------------------------------')
    print(f'Programme excected in {t2 - t1}')

main()