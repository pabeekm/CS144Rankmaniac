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
    # Remove the endline character
    line = line[:-1]

    # Get the iteration number if we see it
    if line.startswith(i_prefix):
        i = int(line.split("\t")[1])
        continue
 
    split = line.split(":")
    split_comma = split[1].split(",")

    # Get the node_id
    node_id = split[0]

    # If this was a pagerank contribution, then add to the node's current pagerarnk
    if int(split_comma[0]) != -1:
        pagerank = float(split_comma[1])
        if node_pageranks.get(node_id) == None:
            node_pageranks[node_id] = alpha * pagerank + (1 - alpha)
        else:
            node_pageranks[node_id] += pagerank * alpha


    # If this was to record previous rank, record the previous rank again
    else:
        prev_rank = split_comma[1]
        prev_pagerank = split_comma[2]
        out_neighbors = split_comma[3:]

        node_prevranks[node_id] = prev_rank
        node_prevpageranks[node_id] = prev_pagerank
        node_outneighbors[node_id] = (",").join(out_neighbors)

# For each key reduced on, output the node_id:    pagerank,prev_ranking,prev_pagerank,out_neighbors
for node_id in node_prevranks.keys():
    if node_outneighbors.get(node_id) != None and node_pageranks.get(node_id) != None:
        sys.stdout.write(node_id + ":\t" + str(node_pageranks[node_id]) + "," +
                     node_prevranks[node_id] + "," + node_prevpageranks[node_id] + "," +
                     node_outneighbors[node_id] + "\n")
    if node_outneighbors.get(node_id) != None and node_pageranks.get(node_id) == None:
        sys.stdout.write(node_id + ":\t" + str(1 - alpha) + "," +
                     node_prevranks[node_id] + "," + node_prevpageranks[node_id] + "," +
                     node_outneighbors[node_id] + "\n")

# Pass along the iteration number
if i is not None:
    sys.stdout.write("$\t%d\n" % (i))
