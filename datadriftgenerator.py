from helpers import *

x_train, y_train = loaddata('D:/Datasets/Poker/poker-hand-training-true.data', True)
x_test, y_test = loaddata('D:/Datasets/Poker/poker-hand-testing.data', True)

print("array_x: ", x_train, "size: ", x_train[0].__len__(), "array_y: ", y_train, "size: ", y_train[0].__len__())