import math
import numpy as np
from data_utilities import *
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from keras import layers

class PricePrediction:
    def __init__(self, ticker):
        self.ticker = ticker
        self.scaler = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.model = None

    def data_preparation(self):
        stock_data = load_file(self.ticker)
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
        model.fit(self.x_train, self.y_train, batch_size= 1, epochs=3)
        self.model = model

    def predict(self):
        model = self.model
        predictions = model.predict(self.x_test)
        predictions = self.scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean(predictions - self.y_test)**2)
        return predictions

prediction = PricePrediction('ETH')
prediction.data_preparation()
prediction.model_creation()
prediction.train_model()
print(len(prediction.predict()))