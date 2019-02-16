#!/usr/bin/env python

import sys

i = 0
i_prefix = "$"

# Each line is formatted NodeId:node_id    rank,prev_rank,[list of neighboring out nodes]
for line in sys.stdin:
    # Get the iteration number if we see it
    if line.startswith(i_prefix):
        i = int(line.split("\t")[1])
        continue

    # Grab the node_id and the values from stdin
    node_id = int((line.split("\t")[0]).split(":")[1])
    vals = (line.split("\t")[1].split(","))

    # This is the pagerank value
    pagerank = float(vals[0])

    # This is the previous ranking, which is either an int from 1-30 or 0
    prev_rank = int(float(vals[1]))

    # These are the outneighbors
    out_neighbors = []
    
    if(len(vals) > 2):
        out_neighbors = [int(x) for x in vals[2:]]

    # This is how much of the pagerank this node gives to each of its neighbors
    contrib = pagerank
    if (len(out_neighbors) != 0):
        contrib = contrib / len(out_neighbors)
    else:
        out_neighbors.append(str(node_id))

    # For each neighbor, output neighbor_id:	node_id, pagerank
    if contrib >= .001:
        for neighbor in out_neighbors:
            sys.stdout.write(str(int(neighbor)) + ":\t" + str(node_id) + "," + 
                             str(contrib) + "\n")

    # For this node, output node_id:	-1,prev_ranking,pagerank,neighbors
    sys.stdout.write(str(node_id) + ":\t-1," + str(prev_rank) + "," + 
                     str(pagerank) + "," + ",".join([str(x) for x in out_neighbors]) 
                     + "\n")

# Pass along the iteration number
sys.stdout.write("$\t%d\n" % (i))
