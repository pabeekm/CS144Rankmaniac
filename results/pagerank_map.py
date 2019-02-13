#!/usr/bin/env python

import sys

#
# This program simply represents the identity function.
#

# Each line is formatted NodeId:node_id    rank,prev_rank,[list of neighboring out nodes]
for line in sys.stdin:
    sys.stdout.write(line)