import numpy as np


def parse(filename):
    points = []
    connections = []
    with open(filename) as f:
        lines = f.readlines()
        
        for line in lines:
            if line[0] == 'v':
                matrix = [float(i) for i in line[2:].split()]
                
                # add w if not present
                if len(matrix) != 4:
                    matrix.append(1)
                    
                points.append(np.matrix(matrix).reshape((4, 1)))
            elif line[0] == 'l':
                connections.append([int(i) for i in line[2:].split()])
            else:
                continue
                
    return points, connections
