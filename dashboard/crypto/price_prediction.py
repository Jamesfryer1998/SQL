import math
import numpy as np
from data_utilities import *
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras import layers
from sklearn.metrics import r2_score

class PricePrediction:
    def __init__(self, ticker, path):
        self.ticker = ticker
        self.path = path
        date = datetime.datetime.now()
        self.date = date.date()
        self.scaler = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.model = None
        self.r2_score = None

    def data_preparation(self):
        stock_data = load_file(self.ticker)
        stock_data.sort_values(by='time', ascending=True, inplace=True)
        close_prices = stock_data['Close']
        values = close_prices.values
        training_data_len = math.ceil(len(values)* 0.8)

        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(values.reshape(-1,1))
        train_data = scaled_data[0: training_data_len, :]
        self.scaler = scaler

        x_train = []
        y_train = []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])
            
        x_train, self.y_train = np.array(x_train), np.array(y_train)
        self.x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        test_data = scaled_data[training_data_len-60: , : ]
        x_test = []
        self.y_test = values[training_data_len:]

        for i in range(60, len(test_data)):
            x_test.append(test_data[i-60:i, 0])

        x_test = np.array(x_test)
        self.x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        return x_test

    def model_creation(self):
        model = keras.Sequential()
        model.add(layers.LSTM(100, return_sequences=True, input_shape=(self.x_train.shape[1], 1)))
        model.add(layers.LSTM(100, return_sequences=False))
        model.add(layers.Dense(25))
        model.add(layers.Dense(1))
        self.model = model

    def train_model(self):
        model = self.model
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(self.x_train, self.y_train, batch_size=32, epochs=75, verbose=0)
        print('Model fitting...')
        print('Model complete, saving predictions.')
        self.model = model

    def predict(self):
        model = self.model
        predictions = model.predict(self.x_test)
        predictions = self.scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean(predictions - self.y_test)**2)
        r2 = r2_score(self.y_test, predictions)

        pred_dict = {
            'time':str(self.date),
            'rmse':rmse,
            'r2_score':r2
        }

        with open(f'{self.path}/{self.ticker}-{self.date}-pred.json', 'w', encoding='utf-8') as file:
            json.dump(pred_dict, file, indent=2)

        print(r2)

prediction = PricePrediction('ETH', '/Users/james/Projects/SQL/Cache/crypto_predictions')
prediction.data_preparation()
prediction.model_creation()
prediction.train_model()
prediction.predict()