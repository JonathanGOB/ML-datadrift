from helpers import *
import numpy as np
import statistics
import random
from progress.bar import Bar


x_test, y_test = loaddata('D:/Datasets/Poker/poker-hand-testing.data', False)
print("array_x: ", x_test, "size: ", x_test[0].__len__(), "array_y: ", y_test, "size: ", y_test[0].__len__())


def categorical(datax, datay, labels):
    window = np.array([[[[] for e in range(0, datax[0].__len__())], [label]] for label in labels])
    for i in range(len(datax)):
        rowx = datax[i]
        rowy = datay[i]
        for p in range(len(rowx)):
            window[rowy][0][0][p].append(rowx[p])

    bar = Bar('calculating mean and standard deviation', max=len(window))

    array_mean = []
    array_std = []

    for i in range(len(window)):
        bar.next()
        array_mean.append(np.mean(window[i][0], axis=1))
        array_std.append(np.std(window[i][0], axis=1))

    array_mean = np.array(array_mean)
    array_std = np.array(array_std)

    bar.finish()
    return array_mean, array_std


def chances(datay, labels, random):
    window = np.array([0 for e in range(len(labels))])
    for i in range(len(datay)):
        window[datay[i]] += 1

    size = len(datay)

    chance_array = []
    bar = Bar('calculating chances', max=len(window))
    for i in range(len(window)):
        bar.next()
        chance_array.append(window[i] / size)

    chance_array = np.array(chance_array)

    if random:
        np.random.shuffle(chance_array)

    bar.finish()
    return chance_array


def generatedatadriftfile(mean, std, amount, chance, labels, type):
    choices = np.random.choice(len(labels), amount, p=chance)
    generated = []
    bar = Bar('generating data drift', max=len(choices))
    for e in choices:
        label_means = mean[e]
        label_stds = std[e]
        modulus = 0
        column = []
        for p in range(len(label_means)):
            if type == "sudden-change":
                binomial = np.random.choice(2, 1, p=[0.5, 0.5])
                value = None
                if binomial == 0:
                    value = label_means[p] - (3 * label_stds[p])

                if binomial == 1:
                    value = label_means[p] + (3 * label_stds[p])

                value = int(value)

                column.append(value)
                modulus += 1

            if type == "gradual-change":
                binomial = np.random.choice(2, 1, p=[0.5, 0.5])
                context_switch = np.random.choice(2, 1, p=[0.5, 0.5])
                value = None
                if context_switch != 1:
                    if binomial == 0:
                        value = label_means[p] - (3 * label_stds[p])

                    if binomial == 1:
                        value = label_means[p] + (3 * label_stds[p])
                else:
                    value = label_means[p]

                value = int(value)

                column.append(value)
                modulus += 1

        bar.next()
        column.append(e)
        generated.append(column)

    generated = np.array(generated)
    np.savetxt('D:/Datasets/Poker/poker-' + type + '.data', generated, fmt='%i', delimiter=',')
    bar.finish()


labels = [e for e in range(0, 10)]

mean, std = categorical(x_test, y_test, labels)
chance = chances(y_test, labels, False)
generatedatadriftfile(mean, std, 1000000, chance, labels, "sudden-change")