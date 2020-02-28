from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from helpers import *

x_train, y_train = loaddata('D:/Datasets/Poker/poker-hand-training-true.data', True)
x_test, y_test = loaddata('D:/Datasets/Poker/poker-hand-testing.data', True)

inputs = keras.Input(shape=(x_train.shape[1],), name="hand")
hiddenlayer = layers.Dense(25, activation='relu', name="dense1")(inputs)
hiddenlayer = layers.Dense(17, activation='relu', name="dense2")(hiddenlayer)
outputs = layers.Dense(y_train.shape[1], name="prediction", activation='sigmoid')(hiddenlayer)

model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer=keras.optimizers.Adam(), loss='mean_squared_error')

print('# Fit model on training data')
history = model.fit(x_train, y_train,
                    batch_size=32,
                    epochs=20,
                    # We pass some validation for
                    # monitoring validation loss and metrics
                    # at the end of each epoch
                    validation_data=(x_test, y_test))

print('\nhistory dict:', history.history)

# Evaluate the model on the test data using `evaluate`
print('\n# Evaluate on test data')
results = model.evaluate(x_test, y_test, batch_size=32)
print('test loss, test acc:', results)
model.save('models/poker_predictor.h5')
