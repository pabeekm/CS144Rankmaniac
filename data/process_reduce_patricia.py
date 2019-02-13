#!/usr/bin/env python

import string
import sys

a = .85
i = 0
# Initialize list of PageRanks
n_max = 500000
ranks = [0.0] * n_max
prefix = "$"
prefix_i = "$$"

# The biggest node id we've seen so far
max_node = 0
# The last node id we read in
last_node = 0
# Running pageRank total for the current node
running_total = 0.0

# The current top-20
highest = []
# The last top-20
last_highest = []
# The adjacency matrix
neighbors = dict()


# Read the input
for line in sys.stdin:
    # Grab out iteration number if we see it
    if line.startswith(prefix_i):
        i = int(line.split("\t")[1])
    # Grab our last top 20 if we see it.
    elif line.startswith(prefix):
        node = int(line.split("\t")[1])
        last_highest.append(node)
    # Keep track of any PageRank contributions we are fed
    else:
        node, source, contribution = line.split("\t")
        node = int(node)
        source = int(source)
        # Record the edge in our adjacency list
        if source in neighbors:
            neighbors[source].append(str(node))
        else:
            neighbors[source] = [str(node)]
        # If we've finised reading a node, write its total contribution
        if node != last_node:
            ranks[last_node] = running_total
            # Add the node to the highest list, if applicable
            if len(highest) < 20:
                highest.append((running_total, last_node))
            else:
                if highest[-1][0] < running_total:
                    highest[-1] = (running_total, last_node)
                highest = sorted(highest, reverse=True)
            running_total = 0.0
            last_node = node
            if node > max_node:
                max_node = node
        running_total += float(contribution)


# Calculate the final total ranks
ranks[max_node] = running_total
for x in range(0, max_node):
    ranks[x] = ranks[x] + ((1.0 - a) / (max_node + 1))


# Get rid of the excess stuff in the highest list
for x in range(0, len(highest)):
    highest[x] = highest[x][1]


# Print the highest values if we are done
i += 1
if (i == 50):
    for id in highest:
        sys.stdout.write("FinalRank:%.1f\t%d\n" % (ranks[id], id))


# Otherwise, pass our current info to the next iteration
else:
    for node, adjacent in neighbors.items():
        adjacency_string = ",".join(adjacent)
        rank = ranks[node]
        sys.stdout.write(":%d\t%.16f,%.16f,%s\n" % (node, rank, rank, adjacency_string))
    sort_helper = list(string.ascii_lowercase)
    for x in range(0, len(highest)):
        sys.stdout.write("$%s\t%d\n" % (sort_helper[x], highest[x]))
    sys.stdout.write("$$\t%d\n" % (i))
