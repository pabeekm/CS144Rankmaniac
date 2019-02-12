#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

# Each line in is node_id    0/1,pagerank/prev_rank

# We can only guarantee that this reducer gets all of the key-val pairs for some particular value, so 
# it could get all of them as well, so we need this dict to keep track of which keys this reducer is 
# "in charge" of
node_pageranks = {}
node_outneighbors = {}
node_prevranks = {}
for line in sys.stdin:
    # Get the node_id
    node_id = int((line.split(":")[0]))

    # If this was a pagerank contribution, then record the this node as an outneighbor for another node and add to the current pagerarnk
    if int((line.split(":")[1].split(",")[0])) != -1:
        in_neighbor = int((line.split(":")[1].split(",")[0]))
        pagerank = float((line.split(":")[1].split(",")[1]))
        if node_pageranks.get(node_id) == None:
            node_pageranks[node_id] = pagerank
        else:
            node_pageranks[node_id] += pagerank

        if node_outneighbors.get(in_neighbor) == None:
            node_outneighbors[in_neighbor] = [node_id]
        else:
            node_outneighbors[in_neighbor].append(node_id)

    # If this was to record previous rank, record the previous rank again
    else:
        prev_rank = int((line.split(":")[1].split(",")[1]))
        node_prevranks[node_id] = prev_rank

# For each key reduced on, output the node_id    pagerank,prev_rank,out_neighbors
for node_id in node_pageranks.keys():
    if node_outneighbors.get(node_id) != None:
        sys.stdout.write(str(node_id) + ":" + str(node_pageranks[node_id]) + "," + 
                     str(node_prevranks[node_id]) + "," + 
                     ",".join([str(x) for x in node_outneighbors[node_id]]) + "\n")
    else:
        sys.stdout.write(str(node_id) + ":" + str(node_pageranks[node_id]) + "," + 
                     str(node_prevranks[node_id]) + "\n")

