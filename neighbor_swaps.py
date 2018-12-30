#!/usr/bin/env python3
import sys, os, random
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

path_weights = [sum(weights[c] for c in p) for p in paths]

def update_lists(i):
    path_centers[i] = find_center(paths[i])
    path_weights[i] = sum(weights[c] for c in paths[i])

def find_neighborhood(i):
    ds = []
    for j in range(len(paths)):
        if j != i:
            d = distances[path_centers[i]][path_centers[j]]
            ds.append([d,j])
    ds.sort()
    ds = [i for [j,i] in ds]
    return ds

path_neighborhood = [find_neighborhood(i) for i in range(len(paths))]

def try_swap(i, ii, j, jj):
    p1, p2 = paths[i], paths[j]
    c1, c2 = paths[i][ii], paths[j][jj]    

    if path_weights[i] + weights[c2] - weights[c1] < C and \
        path_weights[j] + weights[c1] - weights[c2] < C:
            #print("swap %d -> %d" % (i,j))

            d_prev = path_distance(p1) + path_distance(p2)

            p1c = p1.copy()
            p2c = p2.copy()

            p1c[ii] = c2
            p2c[jj] = c1

            opt2(p1c, path_distance)
            opt2(p2c, path_distance)

            d_new = path_distance(p1c) + path_distance(p2c)

            if d_new < d_prev:

                p1[:] = p1c
                p2[:] = p2c

                update_lists(i)
                update_lists(j)

                return True
    return False

#
# Try to swap individual elements in nearby groups
#
def try_pairs(i, j):
    for ii in range(len(paths[i])):
        for jj in range(len(paths[j])):
            if try_swap(i,ii,j,jj):
                return True
    return False

neighborhood_size = 20
while True:
    for i in range(len(paths)):
        j = path_neighborhood[i][random.randint(0,neighborhood_size)]
        try_pairs(i,j)

    path_neighborhood = [find_neighborhood(i) for i in range(len(paths))]

    save(paths)