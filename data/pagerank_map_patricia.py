#!/usr/bin/env python

import sys
import string

a = 0.85
i = 0
prefix = "$"
prefix_i = "$$"
last_highest = []

for line in sys.stdin:
    # Grab the iteration number
    if line.startswith(prefix_i):
        i = int(line.split("\t")[1])
    # Grab last top-20
    elif line.startswith(prefix):
        node = int(line.split("\t")[1])
        last_highest.append(node)
    # Read in the adjacency matrix
    else:
        node, remainder = line.strip().split("\t")
        node = int(node.split(":")[1])
        remainder = remainder.split(",")
        current_rank = float(remainder[0])
        last_rank = float(remainder[1])
        neighbors = remainder[2:]
        # Calculate the node's contribution to each neighbor
        if (len(neighbors) != 0):
            contribution = (current_rank * a) / len(neighbors)
            # Tell the reducer to give the contribution to each neighbor
            for dest in neighbors:
                sys.stdout.write("%s\t%d\t%.16f\n" % (dest, node, contribution))

# Pass along the iteration number
sys.stdout.write("$$\t%d\n" % (i))

# Pass along the last top-20
sort_helper = list(string.ascii_lowercase)
for x in range(0, len(last_highest)):
    sys.stdout.write("$%s\t%d\n" % (sort_helper[x], last_highest[x]))

