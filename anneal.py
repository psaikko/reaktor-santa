#!/usr/bin/env python3
import sys, os, random, math
from itertools import permutations
from kopt import opt2
from common import *

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("need solution file as input")
    exit()

paths = read(sys.argv[1])

# sorted_distances = [sorted((d,i) for (i,d) in enumerate(distances[city][1:],1)) for city in range(N+1)]

# print(sorted_distances[1][:3])

city_path_index = [-1] * (N+1)
for i,path in enumerate(paths):
    for j,city in enumerate(path):
        city_path_index[city] = i

def P(e_old, e_new, t):
    if e_new < e_old: return 1
    else: return math.exp(-(e_new - e_old) / t)

t_max = 10000
i_max = 10000000
cool_rate = (1/t_max)**(1/i_max)

def exp_temperature(i):
    return t_max * cool_rate ** i

def lin_temperature(i):
    return t_max * (i_max - i)/i_max

def neighbour():
    while True:
        city_i = random.randint(2,N)
        city_j = random.randint(2,N)
        if city_i == city_j: continue
        #print(i,j)
        pi = city_path_index[city_i]
        pj = city_path_index[city_j]
        if pi == pj: continue

        wi = sum(weights[c] for c in paths[pi])
        wj = sum(weights[c] for c in paths[pj])

        wii = weights[city_i]
        wjj = weights[city_j]
                        
        if wi - wii + wjj <= C and wj - wjj + wii <= C:
            e_old = path_distance(paths[pi]) + path_distance(paths[pj])

            copy_i = paths[pi].copy()
            copy_j = paths[pj].copy()

            try:
                ii = copy_i.index(city_i)
                jj = copy_j.index(city_j)
            except:
                print(i, pi, copy_i)
                print(j, pj, copy_j)
                exit()

            #print(copy_i)
            tmp = copy_i[ii]
            copy_i[ii] = copy_j[jj]
            copy_j[jj] = tmp
            #print(copy_i)

            e_new = path_distance(copy_i) + path_distance(copy_j)

            e_diff = e_new - e_old

            return e_diff, copy_i, copy_j, pi, pj, city_i, city_j

e_current = sum(path_distance(path) for path in paths)
e_best = e_current

for i_step in range(i_max):
    T = exp_temperature(i_step)

    diff, path_i, path_j, i, j, ci, cj = neighbour()

    e_next = e_current + diff

    if P(e_current, e_next, T) > random.random():
        print("swap",ci,cj)
        #print(path_i)
        #print(path_j)
        paths[i][:] = path_i
        paths[j][:] = path_j
        for c in path_i:
            city_path_index[c] = i
        for c in path_j:
            city_path_index[c] = j
        e_current += diff
        print(e_current, T, i_max - i_step)
        
    if i % 100 == 0:
        if e_current < e_best:
            e_best = e_current
            save(paths)

if e_current < e_best:
    save(paths)