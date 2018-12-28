#!/usr/bin/env python3
import geopy.distance as geodist
import numpy as np
import sys, pickle, os, random
from itertools import permutations
from kopt import opt2

C = 10 * 1000 * 1000 # 10 tons

korvatunturi = [68.073611, 29.315278]

geodist.EARTH_RADIUS = 6378

node_distance = lambda a, b : geodist.great_circle(a,b).meters

locations = {}
weights = {}

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("need solution file as input")
    exit()

if os.path.exists("distances.npy"):
    distances = np.load("distances.npy")
else:
    print("run solve.py to generate distance matrix")
    exit()

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

    if len(l) == 0: return 0

    d = distances[1][l[0]]

    for i in range(1,len(l)):
        d += distances[l[i-1]][l[i]]

    d += distances[l[-1]][1]
    return d

paths = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        path = list(map(int, line.strip().split(";")))
        paths.append(path)

total_d = 0
max_d_sum = 0

#
# Find 'central' city with least distances to other cities
#
def find_center(path):
    min_d = float('inf')
    min_i = -1

    for i,c in enumerate(path):
        d = sum(distances[c][c2] for c2 in path)
        if min_d > d:
            min_d = d
            min_i = i
    
    return path[min_i]

path_centers = [find_center(p) for p in paths]

#
# Find city with greasest sum of distances to other cities
#
def find_outlier(path):
    max_d   = 0
    max_j   = -1

    for j,c in enumerate(path):
        d = sum(distances[c][c2] for c2 in path)
        if d > max_d:
            max_d = d
            max_j = j

    return path[max_j]

path_outliers = [find_outlier(p) for p in paths]

def swap(l,i,j):
    l[i], l[j] = l[j], l[i]

path_weights = [sum(weights[c] for c in p) for p in paths]

def update_lists(i):
    path_outliers[i] = find_outlier(paths[i])
    path_centers[i] = find_center(paths[i])
    path_weights[i] = sum(weights[c] for c in paths[i])

def try_swap(p1, c1, p2, c2):
    i = p1.index(c1)
    j = p2.index(c2)

    p1i = paths.index(p1)
    p2i = paths.index(p2)

    d_prev = path_distance(p1) + path_distance(p2)

    p1[i] = c2
    p2[j] = c1

    d_new = path_distance(p1) + path_distance(p2)

    p1[i] = c1
    p2[j] = c2

    if d_new > d_prev:
        return False

    if path_weights[p1i] + weights[c2] - weights[c1] < C and \
        path_weights[p2i] + weights[c1] - weights[c2] < C:
            print("swap")

            p2.remove(c2)
            p1.append(c2)

            p1.remove(c1)
            p2.append(c1)

            opt2(p1,path_distance)
            opt2(p2,path_distance)

            update_lists(p1i)
            update_lists(p2i)

            return True
    return False

#
# Try to reassign "worst" city of each group
#

improved = True
while improved:
    improved = False
    for i in range(len(paths)):
        for j in range(i+1,len(paths)):
            if distances[path_outliers[i]][path_centers[j]] < distances[path_outliers[i]][path_centers[i]]:
                if path_weights[j] + weights[path_outliers[i]] < C:

                    p1 = paths[i].copy()
                    p2 = paths[j].copy()

                    d_old = path_distance(p1) + path_distance(p2)

                    p1.remove(path_outliers[i])
                    p2.append(path_outliers[i])

                    opt2(p1, path_distance)
                    opt2(p2, path_distance)

                    d_new = path_distance(p1) + path_distance(p2)

                    if d_new < d_old:
                        print("reassign %d -> %d" % (i,j))
                        paths[i][:] = p1
                        paths[j][:] = p2

                        update_lists(i)
                        update_lists(j)

                        improved = True
                        break
                elif distances[path_outliers[j]][path_centers[i]] < distances[path_outliers[j]][path_centers[j]]:
                    # swap outliers?
                    if path_weights[j] + weights[path_outliers[i]] - weights[path_outliers[j]] < C and \
                        path_weights[i] + weights[path_outliers[j]] - weights[path_outliers[i]] < C:
                    
                        p1 = paths[i].copy()
                        p2 = paths[j].copy()

                        d_old = path_distance(p1) + path_distance(p2)

                        p1.remove(path_outliers[i])
                        p2.append(path_outliers[i])

                        p2.remove(path_outliers[j])
                        p1.append(path_outliers[j])

                        d_new = path_distance(p1) + path_distance(p2)

                        if d_new < d_old:
                            print("swap %d -> %d" % (i,j))

                            paths[i][:] = p1
                            paths[j][:] = p2

                            update_lists(i)
                            update_lists(j)

                            improved = True                  
                            break

total = sum(path_distance(p) for p in paths)

print("new distance", total)

with open(str(int(total))+".res", 'w') as f:
    for path in paths:
        pathstr = ";".join(map(str, path))+"\n"
        f.write(pathstr)