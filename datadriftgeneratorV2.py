from helpers import *
from tqdm import tqdm
import numpy as np 
import random

def learnpatterns(x, y, labels):

    patterns = {label: [] for label in labels}
    print(patterns)
    print("sorting patterns")
    for data in tqdm(range(len(x))):
        label = int(y[data])
        patterns_y = patterns[label]
        new_pattern_x = list(x[data])
        patterns[label].append(new_pattern_x)

    print("aggregating patterns")
    for i in tqdm(range(len(patterns))):
        patterns[i] = [list(x) for x in set(tuple(x) for x in patterns[i])]

    return patterns


def generatenormallist(dict_patterns, chances, type):
    return_list = []
    print("generating list")
    for index in tqdm(range(len(chances))):
        y = chances[index]
        x_list = dict_patterns[y]
        choice = random.randint(0, len(x_list) - 1)
        x = list(x_list[choice])
        x.append(y)
        return_list.append(x)

    generated = np.array(return_list)
    print(generated, "size: ", len(generated[0]))
    print("saving file...")
    np.savetxt('D:/Datasets/Poker/poker-' + type + '.data', generated, fmt='%i', delimiter=',')
    print("file saved")

x_test, y_test = loaddata('D:/Datasets/Poker/poker-hand-testing.data', False)
labels = [e for e in range(0, 10)]
chance = chances(y_test, labels, False)
chance = generatelabels(chance, labels, 1000000)
patterns = learnpatterns(x_test, y_test, labels)
generated = patterns
generatenormallist(generated, chance, "normal-data")