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

labels = [e for e in range(0, 10)]

mean, std = categorical(x_test, y_test, labels)
chance = chances(y_test, labels, False)
contextswitcher = sys.argv[3] 
generatedatadriftfile(mean, std, int(sys.argv[2]), chance, labels, sys.argv[1], eval(sys.argv[3]))