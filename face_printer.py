import math

import pygame.draw


def print_faces(projected_points, points, faces, screen, WIDTH, HEIGHT): 
    et, colors = construct_edge_table(faces, projected_points, points, WIDTH, HEIGHT)
    
    # for edge in et:
    #     pygame.draw.line(screen, (0, 0, 255), (edge[2], edge[0]), (edge[2], edge[1]), 10)

    for i in range(HEIGHT):
        # remove all edges that are done
        # print(i)
        at = list(filter(lambda x: x[0] >= i >= x[1], et))
        # update x
        for edge in at:
            edge[2] = (i - edge[7]) / edge[6] if edge[6] != 0 else edge[2]

        at.sort(key=lambda x: x[2])
        print(at)
        
        # fill the pixel
        for j in range(0, len(at) - 1, 1):
            print(at[j])
            print(at[j+1])
            x0 = at[j][2]
            x1 = at[j+1][2]
            pygame.draw.line(screen, colors[at[j][8]], (x0, i), (x1, i), 1)
            

def construct_edge_table(faces, projected_points, points, width, height):
    # [ yMax, yMin, x, sign, dX, dY, a, b, id ]
    et = []
    colors = []
    i = 0
    for face in faces:
        # we assume there are 3
        point0 = projected_points[face[0]]
        point1 = projected_points[face[1]]
        point2 = projected_points[face[2]]
        
        # 0 + 1
        et.append(construct_edge(point0, point1, width, height, i))
        # 0 + 2
        et.append(construct_edge(point0, point2, width, height, i))
        # 1 + 2
        et.append(construct_edge(point1, point2, width, height, i))
        
        colors.append((face[3], face[4], face[5]))
        i += 1
        
    return et, colors


def construct_edge(point0, point1, width, height, id):
    ymax_point = point0 if point0[1] >= point1[1] else point1
    ymin_point = point0 if point0[1] < point1[1] else point1
    dx = (int(point0[0]*width + width/2) - int(point1[0] * width + width/2))
    dy = (int(point0[1]*height + height/2) - int(point1[1] * height + height/2))
    a = dy/dx if dx != 0 else dy
    b = int(ymin_point[1]*height + height/2) - a * int(ymin_point[0] * width + width/2)
    
    return [
        int(ymax_point[1] * height + height/2), # yMax
        int(ymin_point[1] * height + height/2), # yMin
        int(ymin_point[0] * width + width/2), # x
        1 if ymax_point[0] >= ymin_point[0] else -1, # sign
        int(math.fabs(dx)), # dX
        int(math.fabs(dy)),
        a, 
        b,
        id,
    ]
