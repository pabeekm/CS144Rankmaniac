#!/usr/bin/env python

import sys

# Prints a tuple of form (node_id, pagerank, prev_rank, out_neighbors)
def print_node(node, node_list):
    node_id = node[0]
    pagerank = node[1]
    prev_rank = node[2]
    out_neighbors = node[3]

    if(len(out_neighbors) > 0):
        node_list.append("NodeId:" + node_id + "\t" + str(pagerank) + "," + str(prev_rank) + "," + ",".join(out_neighbors) + "\n")
    else:
        node_list.append("NodeId:" + node_id + "\t" + str(pagerank) + "," + str(prev_rank) + "\n")

# Print entire list
def print_nodes(node_list):
    for line in node_list:
        sys.stdout.write(line)

# Prints the final rankings
def print_final(node):
    node_id = node[0]
    pagerank = node[1]

    sys.stdout.write("FinalRank:" + str(pagerank) + "\t" + node_id + "\n")

i = 0
i_prefix = "$"
top_30 = []
current_min = 0
node_list = []
total = 0
total_change = 0
for line in sys.stdin:
    # Remove the endline character
    line = line[:-1]

    # Get the iteration number if we see it
    if line.startswith(i_prefix):
        i = int(line.split("\t")[1])
        continue

    # Grab the node_id and the values from stdin
    vals = (line.split(":")[1].split(","))

    # This is the node_id
    node_id = vals[0]

    # This is the pagerank value
    pagerank = float(vals[1])
    
    # This is the previous ranking, which is either an int from 1-30 or 0
    prev_rank = int(vals[2])

    # This is the previous pagerank
    prev_pagerank = float(vals[3])

    total += prev_pagerank
    total_change += abs(pagerank - prev_pagerank)

    out_neighbors = []
    if(len(vals) > 4):
        out_neighbors = vals[4:]
   

    if len(top_30) < 30:
        top_30.append((node_id, pagerank, prev_rank, out_neighbors))
        if pagerank > current_min:
            current_min = min(top_30, key = lambda node:node[1])[1]
        top_30 = sorted(top_30, key = lambda node:node[1], reverse=True)
    else:
        # If this belongs in the top 30, then kick out the bottom element and put it in and then sort
        if pagerank > current_min:
            kicked_out = top_30.pop()
            print_node(kicked_out, node_list)
            top_30.append((node_id, pagerank, prev_rank, out_neighbors))
            current_min = min(top_30, key = lambda node:node[1])[1]
            top_30 = sorted(top_30, key = lambda node:node[1], reverse=True)
        # Otherwise just print the node since it's not top 30 with the previous rank now as 0
        else:
            print_node((node_id, pagerank, 0, out_neighbors), node_list)

# Now that we have the top 30, check if those pageranks are the same as before, if so, we have found the final rankings
done = True
diff_pageranks = 0
change = 0
if total != 0:
    change = total_change / total

for x in range(0, len(top_30)):
    # Get the node
    node = top_30[x]

    # Get the more specific traits
    node_id = node[0]
    pagerank = node[1]
    prev_rank = node[2]
    out_neighbors = node[3]

    if prev_rank != x + 1:
        done = False

    print_node((node_id, pagerank, x + 1, out_neighbors), node_list)

# If we're actually done, print out the final rankings
if done or i == 49:
    for x in range(0, 20):
        node = top_30[x]
        print_final(node)
else:
    print_nodes(node_list)
    # Pass along the iteration number
    sys.stdout.write("$\t%d\n" % (i + 1))
