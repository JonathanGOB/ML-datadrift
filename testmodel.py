from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow.keras.models import load_model
from helpers import *

x_test, y_test = loaddata('D:/Datasets/Poker/poker-sudden-change.data', True)

loaded = load_model('models/poker_predictor.h5')

# Check its architecture
loaded.summary()

# Evaluate the model on the test data using `evaluate`
print('\n# Evaluate on test data')
results = loaded.evaluate(x_test, y_test, batch_size=32)
print('test loss, test acc:', results)

def historyloss(model, x, y):
    model.predict(x)
