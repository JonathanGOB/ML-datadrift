from helpers import *
from tqdm import tqdm
import numpy as np 
import random
import sys
import settings
import timeit
import copy

def learnpatterns(x, y, labels):

    patterns = {label: [] for label in labels}
    print(patterns)
    print("# Sorting patterns")
    for data in tqdm(range(len(x))):
        label = int(y[data])
        patterns_y = patterns[label]
        new_pattern_x = list(x[data])
        patterns[label].append(new_pattern_x)

    print("# Aggregating patterns")
    for i in tqdm(range(len(patterns))):
        patterns[i] = {hash(x):list(x) for x in set(tuple(x) for x in patterns[i])}

    temp = np.array(patterns)
    return patterns


def generatenormallist(dict_patterns, chances, type, labels, contextswitcher):
    return_list = []
    print("# Generating list")
    count = 1
    on = True
    started = False
    for index in tqdm(range(len(chances))):
        started = False
        if type == "normal-change":
            y = chances[index]
            x_list = dict_patterns[y]
            key = random.choice(list(x_list.keys()))
            x = x_list[key].copy()
            x.append(y)
            return_list.append(x)
        if type == "sudden-change":
            y = copy.deepcopy(chances[index])
            x_list = dict_patterns[y]
            if contextswitcher:
                if not on and not started:     
                    started = True
                    # not_found = True
                    # while not_found:
                    #     C = [random.randint(1, 13) for e in range(5)]
                    #     S = [random.randint(1, 4) for e in range(5)]
                    #     CS = tuple(item for sublist in list((zip(S, C))) for item in sublist)
                    #     CS_HASH = hash(CS)

                    #     if not CS_HASH in x_list:
                    #         not_found = False
                    #         CS = list(CS)
                    #         CS.append(y)
                    #         return_list.append(CS)

                    # fast, but doesnt always mean uniqueness
                    # C = [random.randint(1, 13) for e in range(5)]
                    # S = [random.randint(1, 4) for e in range(5)]
                    # CS = [item for sublist in list(zip(S, C)) for item in sublist]
                    # CS.append(y)
                    # return_list.append(CS)
                    
                    #shift to the right and if end to left essentially changing the patterns
                    old_y = copy.deepcopy(y)
                    if y == len(labels) - 1:
                        y = 0
                    
                    if y < len(labels) - 1:
                        y += 1
                    
                    #print("old y: ", old_y, "new_y: ", y)

                    x_list = dict_patterns[old_y]
                    key = random.choice(list(x_list.keys()))
                    x = copy.deepcopy(x_list[key])
                    x.append(y)
                    return_list.append(x)

                    count += 1
                    if count == settings.N:
                        on = True
                        count = 0

                if on and not started:
                    started = True
                    key = random.choice(list(x_list.keys()))
                    x = copy.deepcopy(x_list[key])
                    x.append(y)
                    return_list.append(x)
                    count += 1
                    if count == settings.K:
                        on = False
                        count = 0
            if not contextswitcher:
                old_y = copy.deepcopy(y)
                if y == len(labels) - 1:
                    y = 0
                
                if y < len(labels) - 1:
                    y += 1
                
                #print("old y: ", old_y, "new_y: ", y)

                x_list = dict_patterns[old_y]
                key = random.choice(list(x_list.keys()))
                x = copy.deepcopy(x_list[key])
                x.append(y)
                return_list.append(x)


    generated = np.array(return_list)
    print(generated, "size: ", len(generated[0]))
    print("saving file...")
    np.savetxt('D:/Datasets/Poker/poker-' + type + '.data', generated, fmt='%i', delimiter=',')
    print("file saved")
if __name__ == '__main__':
    x_test, y_test = loaddata('D:/Datasets/Poker/poker-hand-training-true.data', False)
    labels = [e for e in range(0, 10)]
    chance = chances(y_test, labels, False)
    chance = generatelabels(chance, labels, 1000000)
    patterns = learnpatterns(x_test, y_test, labels)
    generated = patterns
    generatenormallist(generated, chance, sys.argv[1], labels, eval(sys.argv[2]))