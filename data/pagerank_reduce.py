#!/usr/bin/env python

import sys

# Each line in is node_id    0/1,pagerank/prev_rank

# We can only guarantee that this reducer gets all of the key-val pairs for some particular value, so 
# it could get all of them as well, so we need this dict to keep track of which keys this reducer is 
# "in charge" of
node_pageranks = {}
node_outneighbors = {}
node_prevranks = {}
node_prevpageranks = {}
alpha = .85
i = None
i_prefix = "$"

for line in sys.stdin:
    # Get the iteration number if we see it
    if line.startswith(i_prefix):
        i = int(line.split("\t")[1])
        continue
 
    # Get the node_id
    node_id = int((line.split(":")[0]))

    # If this was a pagerank contribution, then record the this node as an outneighbor for another node and add to the current pagerarnk
    if int((line.split(":")[1].split(",")[0])) != -1:
        in_neighbor = int((line.split(":")[1].split(",")[0]))
        pagerank = float((line.split(":")[1].split(",")[1]))
        if node_pageranks.get(node_id) == None:
            node_pageranks[node_id] = alpha * pagerank + (1 - alpha)
        else:
            node_pageranks[node_id] += pagerank * alpha


    # If this was to record previous rank, record the previous rank again
    else:
        prev_rank = int((line.split(":")[1].split(",")[1]))
        prev_pagerank = float((line.split(":")[1].split(",")[2]))
        out_neighbors = line.split(":")[1].split(",")[3:]

        node_prevranks[node_id] = prev_rank
        node_prevpageranks[node_id] = prev_pagerank
        node_outneighbors[node_id] = [int(x) for x in out_neighbors]

# For each key reduced on, output the node_id    pagerank,prev_rank,out_neighbors
for node_id in node_prevranks.keys():
    if node_outneighbors.get(node_id) != None and node_pageranks.get(node_id) != None:
        sys.stdout.write(str(node_id) + ":" + str(node_pageranks[node_id]) + "," + 
                     str(node_prevranks[node_id]) + "," + str(node_prevpageranks[node_id]) + "," + 
                     ",".join([str(x) for x in node_outneighbors[node_id]]) + "\n")
    else:
        if node_outneighbors.get(node_id) == None and node_pageranks.get(node_id) != None:
            sys.stdout.write(str(node_id) + ":" + str(node_pageranks[node_id]) + "," + 
                     str(node_prevranks[node_id]) + str(node_prevpageranks[node_id]) + "," + "\n")
        if node_pageranks.get(node_id) == None and node_outneighbors.get(node_id) != None:
            sys.stdout.write(str(node_id) + ":" + str(1 - alpha) + "," + 
                     str(node_prevranks[node_id]) + "," + str(node_prevpageranks[node_id]) + "," + 
                     ",".join([str(x) for x in node_outneighbors[node_id]]) + "\n")

# Pass along the iteration number
if i is not None:
    sys.stdout.write("$\t%d\n" % (i))
