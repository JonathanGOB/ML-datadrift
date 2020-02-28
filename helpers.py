import numpy as np

from tqdm import tqdm, trange
from tabulate import tabulate
import settings

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
