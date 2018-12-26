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

korvatunturi = [68.073611, 29.315278]

locations = {}

with open("nicelist.txt", 'r') as f:
    for line in f:
        tokens = list(map(float, line.split(";")))
        locations[int(tokens[0])] = list(map(float, tokens[1:3]))

locations[1] = korvatunturi

paths = []

with open(sys.argv[1], 'r') as f:
    for line in f:
        path = list(map(int, line.strip().split(";")))
        paths.append(path)

colors = [(random(),random(),random()) for i in range(len(paths))]

plt.ion()
fix,ax = plt.subplots(figsize=(8, 8))
for lon in np.linspace(-180,180,10):
    ax.clear()
    m = Basemap(projection='ortho', resolution=None, lat_0=10, lon_0=lon)
    m.bluemarble(scale=0.5)
    for (i,path) in enumerate(paths):
        xys = [ m(locations[i][1],locations[i][0]) for i in path ]
        xs, ys = zip(*xys)
        plt.plot(xs, ys, 'ok', markersize='3', color=colors[i])
    plt.pause(0.01)