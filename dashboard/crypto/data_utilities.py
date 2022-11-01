import json
import pandas as pd
import datetime

def open_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def load_file(ticker):
    date = datetime.datetime.now().date()
    try:
        data = pd.read_csv(f'/Users/james/Projects/SQL/Cache/{ticker}-{date}.csv', sep='\t')
        return data
    except:
        raise Exception('Ticker not found')