#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
    print("need solution file as input")
    exit()

visited = set()

trips = 0

for line in open(sys.argv[1], 'r'):
    children = line.strip().split(";")
    for child in children:
        if not int(child) in visited:
            visited.add(int(child))
        else:
            print("Visits %s again" % child)
    trips += 1

print("%d trips" % trips)

for i in range(2,10001+1):
    if i not in visited:
        print("%d not visited" % i)