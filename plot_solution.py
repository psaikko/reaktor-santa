#!/usr/bin/env python3
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
from random import random
from mpl_toolkits.basemap import Basemap

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("need solution file as input")
    exit()

locations = {}

with open("nicelist.txt", 'r') as f:
    for line in f:
        tokens = list(map(float, line.split(";")))
        locations[int(tokens[0])] = list(map(float, tokens[1:3]))

paths = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        path = list(map(int, line.strip().split(";")))
        paths.append(path)

colors = [(random(),random(),random()) for i in range(len(paths))]

fix,ax = plt.subplots(figsize=(8, 8))
for lon in np.linspace(-180,180,20):
    ax.clear()
    m = Basemap(projection='ortho', resolution=None, lat_0=10, lon_0=lon)
    m.bluemarble(scale=0.5)
    for (i,path) in enumerate(paths):
        xys = [ m(locations[i][1],locations[i][0]) for i in path ]
        xs, ys = zip(*xys)
        plt.plot(xs, ys, 'ok', markersize='3', color=colors[i])
        
        xs = [x for x in xs if x < 10e10]
        ys = [y for y in ys if y < 10e10]
        plt.plot(xs, ys, '-', color=colors[i])
    plt.pause(0.01)