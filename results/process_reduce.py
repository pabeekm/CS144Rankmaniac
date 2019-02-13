#!/usr/bin/env python

import sys

num = 0
for line in sys.stdin:
    node_id = int((line.split("\t")[1]).split(":")[1])
    if num < 20: 
        sys.stdout.write("FinalRank:1.0\t" + str(node_id) + "\n")
    num += 1