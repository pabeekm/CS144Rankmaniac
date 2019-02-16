#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

i = None
i_prefix = "$"

for line in sys.stdin:
    # Get the iteration number if we see it
    if line.startswith(i_prefix):
        i = int(line.split("\t")[1])
        continue

    split = line.split(":")
    # Grab the node_id 
    node_id = split[0]

    # Now just use a generic key so the reducer can be in charge of sorting all output and
    # checking whether or not prev_ranks have changed
    sys.stdout.write("key:" + node_id + "," + split[1])

# Pass along the iteration number
if i is not None:
    sys.stdout.write("$\t%d\n" % (i))
