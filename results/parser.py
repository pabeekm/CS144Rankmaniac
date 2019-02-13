import numpy as np

def parse_into_matrix(file):
    with open(file, "r") as f:
        lines = f.readlines()
        P = np.zeros((len(lines), len(lines)), dtype=bool)

        for line in lines:
            node_id = int((line.split("\t")[0]).split(":")[1])
            connections = (line.split("\t")[1].split(","))
            
            for i in range(2, len(connections)):
                P[node_id][int(connections[i])] = 1
    
        return P


