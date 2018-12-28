#!/usr/bin/env python3
import random
from kopt import opt2
from common import *

i = 2 
total = 0
paths = []

free = set(range(2,N+1))

while len(free):
    s = 0
    l = []
    while s < C and len(free):
        closest_i = -1
        closest_d = float('inf')

        for n in free:
            if s + weights[n] < C:
                if not len(l):
                    d = random.randint(0,100)
                else:
                    d = distances[l[-1]][n]
                
                if d < closest_d:
                    closest_d = d
                    closest_i = n

        #print(closest_d, closest_i)
        if closest_i == -1: break

        s += weights[closest_i]
        l += [closest_i]
        free.remove(closest_i)

    if not len(l): break
    
    opt2(l, path_distance)
    total += path_distance(l)
    paths.append(l)
    print(l)
    print(len(free))

save(paths)