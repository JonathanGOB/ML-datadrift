from helpers import *
import numpy as np
import statistics
import random

x_test, y_test = loaddata('D:/Datasets/Poker/poker-hand-testing.data', False)
print("array_x: ", x_test, "size: ", x_test[0].__len__(), "array_y: ", y_test, "size: ", y_test[0].__len__())


def categorical(datax, datay, labels):
    window = np.array([[[[] for e in range(0, datax[0].__len__())], [label]] for label in labels])

    for i in range(len(datax)):
        rowx = datax[i]
        rowy = datay[i]
        for p in range(len(rowx)):
            window[rowy][0][0][p].append(rowx[p])

    array_mean = []
    array_std = []
    for i in range(len(window)):
        array_mean.append(np.mean(window[i][0], axis=1))
        array_std.append(np.std(window[i][0], axis=1))

    array_mean = np.array(array_mean)
    array_std = np.array(array_std)

    return array_mean, array_std

def chances(datay, labels):
    window = np.array([0 for e in range(len(labels))])
    for i in range(len(datay)):
        window[datay[i]] += 1

    size = len(datay)

    chance_array = []
    for i in range(len(window)):
        chance_array.append(window[i] / size)

    chance_array = np.array(chance_array)

    return chance_array

def generatedatadriftfile(mean, std, amount, chance, labels, type):
    choices = np.random.choice(len(labels), amount, p=chance)

    generated = []
    for e in choices:
        label_means = mean[e]
        label_stds = std[e]
        modulus = 0
        column = []
        for p in range(len(label_means)):
            if type == "sudden_change":
                binomial = np.random.choice(2, 1, p=[0.5, 0.5])
                value = None
                if binomial == 0:
                    value = label_means[p] - (1.5 * label_stds[p]) + random.randrange(0, 3)

                if binomial == 1:
                    value = label_means[p] + (1.5 * label_stds[p]) + random.randrange(0, 3)

                value = int(value)

                if modulus % 2 == 0 and value < 1:
                    value = 1

                if modulus % 2 == 0 and value > 4:
                    value = 4

                if modulus % 2 == 1 and value < 1:
                    value = 1

                if modulus % 2 == 1 and value > 13:
                    value = 13

                column.append(value)
                modulus += 1

        column.append(e)
        generated.append(column)

    generated = np.array(generated)
    np.savetxt('D:/Datasets/Poker/poker' + type + '.data', generated, fmt='%i', delimiter=',')



labels = [e for e in range(0, 10)]

mean, std = categorical(x_test, y_test, labels)
chance = chances(y_test, labels)
generatedatadriftfile(mean, std, 100000, chance, labels, "sudden_change")
