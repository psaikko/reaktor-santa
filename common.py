#!/usr/bin/env python3
import geopy.distance as geodist
import numpy as np
import sys, pickle, os, random

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

if os.path.exists("distances.npy"):
    distances = np.load("distances.npy")
else:
    distances = np.ndarray((N+1,N+1), np.float)
    for i in range(1,N+1):
        print(i)
        for j in range(i+1,N+1):
            distances[i][j] = distances[j][i] = node_distance(locations[i], locations[j])
    np.save("distances", distances)

def path_distance(l):
    global distances
    if len(l) == 0: return 0
    d = distances[1][l[0]]

    for i in range(1,len(l)):
        d += distances[l[i-1]][l[i]]
    
    d += distances[l[-1]][1]
    return d

def save(paths):
    total = sum(path_distance(p) for p in paths)

    filename = str(int(total))+".res" 
    print("saving "+filename)
    
    with open(filename, 'w') as f:
        for path in paths:
            pathstr = ";".join(map(str, path))+"\n"
            f.write(pathstr)
    return filename

def read(filename):
    paths = []
    with open(filename, 'r') as f:
        for line in f:
            path = list(map(int, line.strip().split(";")))
            paths.append(path)
    return paths