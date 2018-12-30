#!/usr/bin/env python3
import sys, os, random
from itertools import permutations
from kopt import opt3
from common import *

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("need solution file as input")
    exit()

paths = read(sys.argv[1])

for i in range(len(paths)):
    opt3(paths[i], path_distance)

save(paths)