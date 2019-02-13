#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

i = 0
i_prefix = "$"

for line in sys.stdin:
    # Get the iteration number if we see it
    if line.startswith(i_prefix):
        i = int(line.split("\t")[1])
        continue

    # Grab the node_id 
    node_id = int((line.split(":")[0]))

    # Now just use a generic key so the reducer can be in charge of sorting all output and
    # checking whether or not prev_ranks have changed
    sys.stdout.write("key:" + str(node_id) + "," + line.split(":")[1])

# Pass along the iteration number
sys.stdout.write("$\t%d\n" % (i))
