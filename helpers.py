import numpy as np

from tqdm import tqdm, trange
from tabulate import tabulate
import settings
import random

# bad example of bit pusher
def number_to_bitarray(array, modulo):
    holder_x = []
    temp_holder_x = ""
    mod_x = 0
    max = 0
    for card in array:
        bits = 0
        if modulo:
            bits = 1 | bits
            if (mod_x % 2) == 1:
                max = 13
            if (mod_x % 2) == 0:
                max = 4
            mod_x += 1
        if not modulo:
            if card == 0:
                bits = 0
            elif card > 0:
                bits = 1 | bits
            max = 10

        card = max - card
        bits = bits << card

        bits = bin(bits)[2:].zfill(max)
        temp_holder_x += bits

    for bit in temp_holder_x:
        holder_x.append(int(bit))

    return holder_x

# returns mean and standard deviation for every column in every possible label
def categorical(datax, datay, labels):
    window = np.array([[[[] for e in range(0, datax[0].__len__())], [label]] for label in labels])

    print("# Collecting all columns for mean and standard deviation")
    for i in tqdm(range(len(datax))):
        rowx = datax[i]
        rowy = datay[i]
        for p in range(len(rowx)):
            window[rowy][0][0][p].append(rowx[p])

    array_mean = []
    array_std = []

    print("# Creating mean and standard deviation")
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

    print("# Creating probabilities per column")
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

def generatelabels(chance, labels, amount):
    choices = []

    print("# Generating labels with the probabilities")
    for i in tqdm(range(amount)):
        choices.append(random.choices(labels, chance)[0])

    return choices

# generates datadrift with the mean, std, amount of rows, chances per label, label itself and type of drift
def generatedatadriftfile(mean, std, amount, chance, labels, type, contextswitcher):
    choices = []

    print("# Generating labels with the probabilities")
    for i in tqdm(range(amount)):
        choices.append(random.choices(labels, chance)[0])

    generated = []
    on = False
    print("# Generating {0} data drift".format(type))
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
                if type == "normal-change-noise":
                    # mean plus noise
                    value = label_means[p] + random.randint(0, int(label_stds[p]))
                    column.append(value)
                if type == "normal-change":
                    # mean plus noise
                    value = label_means[p]
                    column.append(value)

        count += 1
        column.append(choices[e])
        generated.append(column)

    generated = np.array(generated)
    print("saving file...")
    np.savetxt('D:/Datasets/Poker/poker-' + type + '.data', generated, fmt='%i', delimiter=',')
    print("file saved")

# loads number to bit and pushes them to the right without overflow
# also has a signed bit at the beginning for negative numbers
def improved_number_to_bit_array(array, modulo):
    holder = []
    temp_holder = ""
    maximum = 0
    mod = 0
    for card in array:
        bits = 0
        complement = 0
        if modulo:
            if card < 0:
                complement = 1

            if (mod % 2) == 1:
                bits = settings.SBits | bits
                maximum = settings.S
            if (mod % 2) == 0:
                bits = settings.CBits | bits
                maximum = settings.C

            mod += 1

        if not modulo:
            bits = settings.LBits | bits

            if card < 0:
                complement = 1

            maximum = settings.L

        card = abs(card)
        temp_maximum = maximum - 1

        if card != 0:
            if temp_maximum >= card:
                bits = bits >> card

            elif temp_maximum < card:
                trigger = False
                orbits = 0
                while not trigger:
                    copy_bits = bits
                    if temp_maximum < card:
                        copy_bits = copy_bits >> temp_maximum
                    elif temp_maximum >= card:
                        copy_bits = copy_bits >> card

                    if card - temp_maximum < 0:
                        trigger = True

                    orbits = orbits | copy_bits
                    card = card - temp_maximum
                    temp_maximum -= 1

                bits = orbits

        bits = bin(complement)[2:] + bin(bits)[2:].zfill(maximum)
        temp_holder += bits

    for bit in temp_holder:
        holder.append(int(bit))

    return holder

def loaddata(location, bits):

    # load datasets and converts them to bits if true
    learning_set = open(location, 'r')
    num_lines = sum(1 for line in open(location))
    lines = learning_set.readline()
    x = []
    y = []

    once = False
    print("loading dataset {0}. bits on? {1}".format(location, bits))
    with trange(num_lines) as t:
        for i in t:
            container = list(map(int, lines.split(",")))

            if (bits):
                x.append(improved_number_to_bit_array(container[:-1], True))
                y.append(improved_number_to_bit_array(container[-1:], False))

            if not bits:
                x.append(container[:-1])
                y.append(container[-1:])

            lines = learning_set.readline()

    x = np.array(x)
    y = np.array(y)

    print(tabulate([["x", len(x), len(x[0]), x[0]], ["y", len(y), len(y[0]), y[0]]], headers=["name", "total length", "row length", "row example"], tablefmt='orgtbl'))

    return x, y


#splits list in half
def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]
