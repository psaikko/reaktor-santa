#!/usr/bin/env python3
import geopy.distance as geodist
import sys
import pickle
import numpy as np
import os

C = 10 * 1000 * 1000 # 10 tons

korvatunturi = [68.073611, 29.315278]

geodist.EARTH_RADIUS = 6378
node_distance = lambda a, b : geodist.great_circle(a,b).meters

locations = {}
weights = {}

with open("nicelist.txt", 'r') as f:
    for line in f:
        tokens = list(map(float, line.split(";")))
        locations[int(tokens[0])] = list(map(float, tokens[1:3]))
        weights[int(tokens[0])] = int(tokens[3])

locations[1] = korvatunturi
weights[1] = 0

N = max(locations.keys())

def path_distance(l):
    global distances
    d = distances[1][l[0]]

    for i in range(1,len(l)):
        d += distances[l[i-1]][l[i]]

    d += distances[l[-1]][1]
    return d

def swap(l,i,j):
    l[i], l[j] = l[j], l[i]

def opt2(l):
    l = [1] + l + [1]
    d = path_distance(l)
    opt = False
    while not opt:
        opt = True
        for i in range(len(l)):
            for j in range(i+1, len(l)):


                swap(l, i, j)
                ds = path_distance(l)
                if ds < d:
                    #opt = False
                    d = ds
                else:
                    swap(l, i, j)
    l = [1:-1]

i = 2 
total = 0
paths = []

free = set(range(2,N+1))

if os.path.exists("distances.npy"):
    distances = np.load("distances.npy")
else:
    distances = np.ndarray((N+1,N+1), np.float)
    for i in range(1,N+1):
        print(i)
        for j in range(i+1,N+1):
            distances[i][j] = distances[j][i] = node_distance(locations[i], locations[j])
    np.save("distances", distances)

while len(free):
    s = 0
    l = []
    while s < C and len(free):
        closest_i = -1
        closest_d = float('inf')

        for n in free:
            if s + weights[n] < C:
                l.append(n)
                
                opt2(l)
                d = path_distance(l)
                
                if d < closest_d:
                    closest_d = d
                    closest_i = n

                l.remove(n)

        #print(closest_d, closest_i)

        if closest_i == -1: break

        s += weights[closest_i]
        l += [closest_i]
        free.remove(closest_i)

    if not len(l): break
    
    opt2(l)
    total += path_distance(l)
    paths.append(l)
    print(l)
    print(len(free))

with open(str(int(total))+".res", 'w') as f:
    for path in paths:
        pathstr = ";".join(map(str, path))+"\n"
        f.write(pathstr)

print(int(total))
