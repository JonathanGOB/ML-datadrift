import time

from helpers import *
import numpy as np
import statistics
import random
from tqdm import tqdm
import threading
import sys
import settings

x_test, y_test = loaddata('D:/Datasets/Poker/poker-hand-testing.data', False)

# returns mean and standard deviation for every column in every possible label
def categorical(datax, datay, labels):
    window = np.array([[[[] for e in range(0, datax[0].__len__())], [label]] for label in labels])

    print("collecting all columns for mean and standard deviation")
    for i in tqdm(range(len(datax))):
        rowx = datax[i]
        rowy = datay[i]
        for p in range(len(rowx)):
            window[rowy][0][0][p].append(rowx[p])

    array_mean = []
    array_std = []

    print("creating mean and standard deviation")
    for i in tqdm(range(len(window))):
        array_mean.append(np.mean(window[i][0], axis=1))
        array_std.append(np.std(window[i][0], axis=1))

    array_mean = np.array(array_mean)
    array_std = np.array(array_std)

    return array_mean, array_std

# calculates the chances per label
def chances(datay, labels, random):
    window = np.array([0 for e in range(len(labels))])
    for i in range(len(datay)):
        window[datay[i]] += 1

    size = len(datay)

    chance_array = []

    print("creating probabilities per column")
    for i in tqdm(range(len(window))):
        chance_array.append(window[i] / size)

    chance_array = np.array(chance_array)

    if random:
        np.random.shuffle(chance_array)

    return chance_array

def suddenchange(mean, std):
    binomial = random.choices([0, 1], [0.5, 0.5], k=1)[0]
    value = None
    if binomial == 0:
        value = mean - (settings.suddenchange * std)
    if binomial == 1:
        value = mean + (settings.suddenchange * std)
    
    value = int(value)
    return value

def gradualchange(mean, std):
    binomial = random.choices([0, 1], [0.5, 0.5], k=1)[0]
    context_switch = random.choices([0, 1], [0.5, 0.5], k=1)[0]
    value = None
    if context_switch != 1:
        if binomial == 0:
            value = mean - (settings.gradualchange * std)

        if binomial == 1:
            value = mean + (settings.gradualchange * std)
    else:
        value = mean

    value = int(value)
    return value

def incrementalchange(mean, std , index):
    mean[p] = mean[index] + (settings.incrementchange * mean[index])
    value = int(mean[index])
    return value

# generates datadrift with the mean, std, amount of rows, chances per label, label itself and type of drift
def generatedatadriftfile(mean, std, amount, chance, labels, type, contextswitcher):
    choices = []

    print("generating labels with the probabilities")
    for i in tqdm(range(amount)):
        choices.append(random.choices(labels, chance)[0])

    generated = []
    on = False
    print("generating {0} data drift".format(type))
    count = 1
    for e in tqdm(range(len(choices))):
        label_means = mean[choices[e]]
        label_stds = std[choices[e]]
        column = []
        for p in range(len(label_means)):
            if on and contextswitcher:
                if type == "sudden-change":
                    column.append(suddenchange(label_means[p], label_stds[p]))

                if type == "gradual-change":
                    column.append(gradualchange(label_means[p], label_stds[p]))
        
                if type == "incremental-change":
                    column.append(incrementalchange(label_means, label_stds, p))

                if count == settings.N:
                    print("switcher N")
                    count = 0
                    on = False

            elif not on and contextswitcher:
                # mean plus noise
                value = label_means[p] + random.randint(0, int(label_stds[p]))
                column.append(value)
                if count == settings.K:
                    print("switcher K")
                    count = 0
                    on = True
            
            elif not contextswitcher:
                if type == "sudden-change":
                    column.append(suddenchange(label_means[p], label_stds[p]))

                if type == "gradual-change":
                    column.append(gradualchange(label_means[p], label_stds[p]))
        
                if type == "incremental-change":
                    column.append(incrementalchange(label_means, label_stds, p))

        count += 1
        column.append(choices[e])
        generated.append(column)

    generated = np.array(generated)
    print("saving file...")
    np.savetxt('D:/Datasets/Poker/poker-' + type + '.data', generated, fmt='%i', delimiter=',')
    print("file saved")


labels = [e for e in range(0, 10)]

mean, std = categorical(x_test, y_test, labels)
chance = chances(y_test, labels, False)
contextswitcher = sys.argv[3] 
generatedatadriftfile(mean, std, int(sys.argv[2]), chance, labels, sys.argv[1], eval(sys.argv[3]))