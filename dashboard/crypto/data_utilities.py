import json
import pandas as pd
import datetime
import os
import re

def open_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def load_file(ticker):
    date = datetime.datetime.now().date()
    try:
        data = pd.read_csv(f'/Users/james/Projects/SQL/Cache/crypto_data/{ticker}-{date}.csv', sep='\t')
        return data
    except:
        raise Exception('Ticker not found')

def remove_files(file_path):
    time = datetime.datetime.now()
    files = os.listdir(file_path)
    for file in files:
        search = re.search(f'{time.date()}', file)
        if search == None:
            os.remove(f'{file_path}/{file}')
            print(f'{file} removed')