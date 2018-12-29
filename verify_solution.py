#!/usr/bin/env python3
import sys
import os
from common import *

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("need solution file as input")
    exit()

visited = set()

paths = read(sys.argv[1])

print(len(paths),"paths")

for path in paths:
    for child in path:
        if not int(child) in visited:
            visited.add(int(child))
        else:
            print("Visits %s again" % child)

loads = [sum(weights[c] for c in path) for path in paths]

for load in loads:
    if load > C:
        print("overload", load)
        break

for i in range(2,10001+1):
    if i not in visited:
        print("%d not visited" % i)