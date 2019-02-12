#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

# Prints a tuple of form (node_id, pagerank, prev_rank, out_neighbors)
def print_node(node):
    node_id = node[0]
    pagerank = node[1]
    prev_rank = node[2]
    out_neighbors = node[3]

    if(len(out_neighbors) > 0):
        sys.stdout.write("NodeId:" + str(node_id) + "\t" + str(pagerank) + "," + str(prev_rank) + "," + ",".join(out_neighbors))
    else:
        sys.stdout.write("NodeId:" + str(node_id) + "\t" + str(pagerank) + "," + str(prev_rank) + "\n")

# Prints the final rankings
def print_final(node):
    node_id = node[0]
    pagerank = node[1]
    prev_rank = node[2]
    out_neighbors = node[3]

    sys.stdout.write("FinalRank:" + str(pagerank) + "\t" + str(node_id) + "\n")

top_20 = []
current_min = 0
for line in sys.stdin:
    sys.stderr.write("Current min: " + str(current_min) + "\n")
     # Grab the node_id and the values from stdin
    vals = (line.split(":")[1].split(","))

    # This is the node_id
    node_id = int(vals[0])

    # This is the pagerank value
    pagerank = float(vals[1])
    
    # This is the previous ranking, which is either an int from 1-20 or 0
    prev_rank = int(vals[2])
    out_neighbors = []
    if(len(vals) > 3):
        out_neighbors = vals[3:]
   

    if len(top_20) < 20:
        top_20.append((node_id, pagerank, prev_rank, out_neighbors))
        if pagerank > current_min:
            current_min = min(top_20, key = lambda node:node[1])[1]
        top_20 = sorted(top_20, key = lambda node:node[1], reverse=True)
    else:
        # If this belongs in the top 20, then kick out the bottom element and put it in and then sort
        sys.stderr.write("Pagerank: " + str(pagerank) + "\n")
        if pagerank > current_min:
            kicked_out = top_20.pop()
            print_node(kicked_out)
            top_20.append((node_id, pagerank, prev_rank, out_neighbors))
            current_min = min(top_20, key = lambda node:node[1])[1]
            top_20 = sorted(top_20, key = lambda node:node[1], reverse=True)
        # Otherwise just print the node since it's not top 20 with the previous rank now as 0
        else:
            print_node((node_id, pagerank, 0, out_neighbors))

# Now that we have the top 20, check if those pageranks are the same as before, if so, we have found the final rankings
done = True
diff_pageranks = 0
for i in range(0, 20):
    # Get the node
    node = top_20[i]

    # Get the more specific traits
    node_id = node[0]
    pagerank = node[1]
    prev_rank = node[2]
    out_neighbors = node[3]

    if prev_rank != i + 1:
        done = False

    print_node((node_id, pagerank, i + 1, out_neighbors))

# If we're actually done, print out the final rankings
if done:
    for node in top_20:
        print_final(node)

