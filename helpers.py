import numpy as np


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
        try:
            bits = bits << card
        except:
            print("bits: ", bits, "card: ", card, "max: ", max)

        bits = bin(bits)[2:].zfill(max)
        temp_holder_x += bits

    for bit in temp_holder_x:
        holder_x.append(int(bit))

    return holder_x


def loaddata(location, bits):
    # load datasets
    learning_set = open(location, 'r')
    lines = learning_set.readline()
    x = []
    y = []

    once = False
    while lines:
        container = list(map(int, lines.split(",")))

        if(bits):
            x.append(number_to_bitarray(container[:-1], True))
            y.append(number_to_bitarray(container[-1:], False))

        if not bits:
            x.append(container[:-1])
            y.append(container[-1:])

        lines = learning_set.readline()

    x = np.array(x)
    y = np.array(y)

    return x, y


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]