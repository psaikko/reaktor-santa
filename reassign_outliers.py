#!/usr/bin/env python3
import geopy.distance as geodist
import numpy as np
import sys, pickle, os, random
from itertools import permutations
from kopt import opt2
from common import *

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("need solution file as input")
    exit()

paths = read(sys.argv[1])

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

path_weights = [sum(weights[c] for c in p) for p in paths]

def update_lists(i):
    path_outliers[i] = find_outlier(paths[i])
    path_centers[i] = find_center(paths[i])
    path_weights[i] = sum(weights[c] for c in paths[i])

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

save(paths)