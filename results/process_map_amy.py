#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

for line in sys.stdin:
    # Grab the node_id 
    node_id = int((line.split(":")[0]))

    # Now just use a generic key so the reducer can be in charge of sorting all output and
    # checking whether or not prev_ranks have changed
    sys.stdout.write("key:" + str(node_id) + "," + line.split(":")[1])
