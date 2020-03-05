from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow import keras
from helpers import *
from collections import Counter
from tqdm import tqdm
import matplotlib.pyplot as plt

def historyloss(predicted_y, truth_y):
    error = []
    error_history = []
    ones = 0
    zeros = 0
    print("# calculating errors")
    for e in tqdm(range(len(y_predicted))):
        truth = np.array_equal(predicted_y[e], truth_y[e])
        if truth:
            error.append(0)
        if not truth:
            error.append(1)
    print("# calculating history error")
    for e in tqdm(range(len(error))):
        if error[e] == 1:
            ones += 1
        if error[e] == 0:
            zeros += 1
        
        total = zeros + ones
        error_history.append(ones / total)

    return error, error_history

x_test, y_test = loaddata('D:/Datasets/Poker/poker-sudden-change.data', True)

model = load_model('models/poker_predictor.h5')

# Check its architecture
model.summary()

model.compile(optimizer=keras.optimizers.Adam(), loss='mean_absolute_percentage_error')

#Evaluate the model on the test data using `evaluate`
print('\n# Evaluate on test data')
results = model.evaluate(x_test, y_test, batch_size=32)
print('test loss, test acc:', results)
print("# predicting")
y_predicted = model.predict(x_test, batch_size=32, verbose=1)
n = len(y_predicted[0])
y_predicted = np.eye(n, dtype=int)[np.argmax(y_predicted, axis=1)]
y_predicted = tf.keras.backend.eval(y_predicted)

errors, error_history = historyloss(y_predicted, y_test)

y = error_history
x = range(1, len(error_history) + 1)
plt.plot(x, y, marker='o', linestyle='--', color='r', label='mean_absolute_percentage_error')
plt.xlabel('examples')
plt.ylabel('percentage errors overtime') 
plt.title('sudden drift on a poker AI')
plt.legend()
plt.show()
