from turtle import down
import numpy as np
import pandas as pd
import datetime
import yfinance as yf
import os

class downloadData:
    def __init__(self, file_path=None):
        self.time = datetime.datetime.now()
        self.file_path = file_path
        self.file = None
    
    def download_save_data(self, ticker, period, recent_first=False):
        date = self.time.date()
        file = f'{ticker}-{date}'
        print('Initializing search...')

        if os.path.isfile(f'{self.file_path}/{file}.csv') == True:
            print('File exists - No download required.')
        else:
            print(f'Downloading {ticker}-USD - {period}')
            ticker_data = yf.Ticker(f'{ticker}-USD')
            historical_data = ticker_data.history(period=period)
            df = pd.DataFrame(historical_data)
            df.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)
            df.index.rename('time', inplace=True)
            df.index = pd.to_datetime(df.index)
            df.dropna()

            if len(df) == 0:
                raise Exception('No data found')

            if self.file_path == None:
                raise Exception('Please specify file path.')
        
            df.to_csv(f'{self.file_path}/{file}.csv', sep='\t', encoding='utf-8')

        self.file = file

    def load_data(self):
        data = pd.read_csv(f'{self.file_path}/{self.file}.csv', sep='\t')
        return data

# download = downloadData('Cache')
# download.download_save_data('ETH', 'ytd')
# data = download.load_data()
# print(data)