#!/usr/bin/env python3
import sys, os, random
from itertools import permutations
from kopt import opt2
from common import *

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("need solution file as input")
    exit()

paths = read(sys.argv[1])

while True:
    for i in range(len(paths)):
        print(i)
        wi = sum(weights[c] for c in paths[i])
        di = path_distance(paths[i])

        for ii in range(len(paths[i])):
            wii = weights[paths[i][ii]]

            for j in range(i+1, len(paths)):
                wj = sum(weights[c] for c in paths[j])
                dj = path_distance(paths[j])

                for jj in range(len(paths[j])):
                    wjj = weights[paths[j][jj]]
                    
                    if wi - wii + wjj <= C and wj - wjj + wii <= C:
                        pi = paths[i].copy()
                        pj = paths[j].copy()
                        pi[ii], pj[jj] = pj[jj], pi[ii]

                        # opt2(pi, path_distance)
                        # opt2(pj, path_distance)

                        if path_distance(pi) + path_distance(pj) < di + dj:
                            print("swap")
                            paths[i][:] = pi
                            paths[j][:] = pj

                            wi = sum(weights[c] for c in paths[i])
                            wj = sum(weights[c] for c in paths[j])

                            di = path_distance(paths[i])
                            dj = path_distance(paths[j])

                            wii = weights[paths[i][ii]]
    save(paths)