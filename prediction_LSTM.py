# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:33:38 2021

@author: almen
"""

import pandas as pd
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import BatchNormalization, Dense, Cropping1D, LSTM
from tensorflow.keras.models import Sequential
from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler
from numpy.random import seed

seed(1)

# Función para más adelante
def split_sequences(data, n_steps, horizonte, target_list):
    # Predicción para el siguiente valor de todas las columnas
    # Transformar a un array de numpy
    targets = np.array([data.columns.get_loc(c) for c in target_list])
    sequences = data.to_numpy()
    x, y = list(), list()
    # Iteración línea a línea (time_step=1)
    for i in range(len(sequences)):
        # Comprobar si el final se pasa del tamaño del dataset
        end_ix = i + n_steps
        if end_ix + horizonte >= len(sequences):
            break
        # Agrupar el input y el output
        seq_x = sequences[i:end_ix, ]
        seq_y = sequences[end_ix : end_ix + horizonte, targets]  # horizon=1 -> end_ix -1 + horizon
        x.append(seq_x)
        y.append(seq_y)
    return np.array(x), np.array(y)

# Cargar los datos y preparar el dataframe
path = "positivos_por_edificio.csv"
data = pd.read_csv(path, sep=";")

# Normalizar los datos
scaler = MinMaxScaler()
cols = data.columns
indx = data.index
scaled_data = scaler.fit_transform(data)
data = pd.DataFrame(scaled_data, columns=cols)
data.set_index(indx, inplace=True)

# Separar en test y training
sep = int(len(data) * 0.8)
training_data = data.iloc[0:sep]
testing_data = data.iloc[sep:]

# Parametros utilizados
window = 8
horizon = 7

targets = data.columns

# Obtener los time_steps
x_train, y_train = split_sequences(training_data, window, horizon, targets)
x_test, y_test = split_sequences(testing_data, window, horizon, targets)
print(x_train.shape)
print(y_train.shape)

# Entrenar y validar el modelo
model = Sequential()
model.add(BatchNormalization(input_shape=(window, x_train.shape[2], )))

model.add(LSTM(50, return_sequences=True, activation="relu"))
model.add(BatchNormalization())
model.add(LSTM(50, return_sequences=True, activation="relu"))
model.add(BatchNormalization())
model.add(LSTM(50, return_sequences=True, activation="relu"))
model.add(BatchNormalization())

model.add(LSTM(y_train.shape[2], activation="relu", return_sequences=True))
model.add(BatchNormalization())
model.add(Cropping1D((x_train.shape[1]-horizon, 0)))
model.add(BatchNormalization())
model.add(Dense(len(targets)))
model.compile(optimizer=Adam(lr=1e-2), loss="mse")
model.summary()
history = model.fit(x_train, y_train, epochs=400, batch_size=window*10, validation_data=(x_test, y_test), verbose=2)
pyplot.plot(history.history["loss"])
pyplot.plot(history.history["val_loss"])
pyplot.title("model train vs validation loss")
pyplot.ylabel("loss")
pyplot.xlabel("epoch")
pyplot.legend(["train", "validation"], loc="upper right")
pyplot.show()

# Resultados de predicción
data1 = x_test[0]
pred = model.predict(data1.reshape(1, x_test[0].shape[0], x_test[0].shape[1]))

pred = pred.squeeze()

# Des-normalizar
pred = scaler.inverse_transform(pred)

# Transformar en un DataFrame de Pandas
pred = pd.DataFrame(data=pred, columns=cols)
# Guardar en formato CSV
pred.to_csv("predicciones.csv", sep = ";")