import numpy as np


def parse(filename):
    points = []
    connections = []
    faces = []
    with open(filename) as f:
        lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.split()[0] == 'v':
                matrix = [float(i) for i in line[2:].split()]
                
                # add w if not present
                if len(matrix) != 4:
                    matrix.append(1)
                    
                points.append(np.matrix(matrix).reshape((4, 1)))
            elif line.split()[0] == 'l':
                connections.append([int(i) for i in line[2:].split()])
            elif line.split()[0] == 'f':
                faces.append([int(i) for i in line[2:].split()])
            else:
                continue
                
    while len(connections) < len(points):
        connections.append([])
        
    return points, connections, faces
