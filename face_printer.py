import math

import pygame.draw


def print_faces(projected_points, points, faces, screen, WIDTH, HEIGHT): 
    et, polygons = construct_edge_table(faces, projected_points, points, WIDTH, HEIGHT)
    # print(len(et))
    # pygame.draw.circle(screen, (253, 255, 255), (700, 450), 1)
    # print(polygons)
    
    for i in range(HEIGHT):
        # remove all edges that are done
        # print(i)
        at = list(filter(lambda x: x[0] >= i >= x[1], et))
        # update x
        for edge in at:
            edge[2] = (i - edge[7]) / edge[6] if edge[6] != 0 else edge[2]

        at.sort(key=lambda x: x[2])
        # print(at)
        # get max x of every polygon
        for polygon in polygons:
            xs = list(map(lambda x: x[2], list(filter(lambda x: x[8] == polygons.index(polygon), at))))
            polygon[5] = max(xs) if len(xs) > 0 else 0
            polygon[6] = min(xs) if len(xs) > 0 else 0
        
        # fill the pixel
        for j in range(0, len(at) - 1, 1):
            x0 = at[j][2]
            x1 = at[j+1][2]
            active_polygons = list(filter(lambda x: x[5] > x0 >= x[6], polygons))
            # if there are more polygons here -> sort by depth
            if len(active_polygons) == 0:
                continue
            elif len(active_polygons) == 1:
                # pygame.draw.line(screen, polygons[at[j+1][8]][4], (x0, i), (x1, i), 1)
                pygame.draw.line(screen, active_polygons[0][4], (x0, i), (x1, i), 1)
            else:
                tempy = (i - HEIGHT/2) / HEIGHT
                tempx0 = (x0 - WIDTH/2) / WIDTH
                tempx1 = (x1 - WIDTH/2) / WIDTH
                depths_min = list(map(lambda p: [((-p[0] * tempx0 - p[1] * tempy - p[3]) / p[2]) if p[2] != 0 else p[7], p[4]], active_polygons))
                depths_max = list(map(lambda p: [((-p[0] * tempx1 - p[1] * tempy - p[3]) / p[2]) if p[2] != 0 else p[7], p[4]], active_polygons))
                depths_min.sort(key=lambda lmao: math.fabs(float(lmao[0])), reverse=True)
                depths_max.sort(key=lambda lmao: math.fabs(float(lmao[0])), reverse=True)
                # print(list(map(lambda lmao: float(lmao[0]), depths_min)))
                if depths_min[0][0] == depths_max[0][0]:
                    # print(active_polygons)
                    color = depths_min[0][1]
                    pygame.draw.line(screen, color, (x0, i), (x1, i), 1)
                    continue
                # color = depths_min[0][1]
                # pygame.draw.line(screen, color, (x0, i), (x1, i), 1)
                # continue
                for x in range(int(x0), int(x1)):
                    tempy = (i - HEIGHT/2) / HEIGHT
                    tempx = (x - WIDTH/2) / WIDTH
                    # print(tempx, tempy)
                    depths = list(map(lambda p: [((-p[0] * tempx - p[1] * tempy - p[3]) / p[2]) if p[2] != 0 else p[7], p[4]], active_polygons))
                    depths.sort(key=lambda lmao: math.fabs(float(lmao[0])), reverse=True)
                    # print(list(map(lambda lmao: float(lmao[0]), depths)))
                    if depths[0][0] == depths[1][0]:
                        x_start = x
                        while depths[0][0] == depths[1][0] and x < x1:
                            x += 1
                            tempx = (x - WIDTH/2) / WIDTH
                            depths = list(map(lambda p: [((-p[0] * tempx - p[1] * tempy - p[3]) / p[2]) if p[2] != 0 else p[7], p[4]], active_polygons))
                            depths.sort(key=lambda lmao: math.fabs(float(lmao[0])), reverse=True)
                        if x_start != x:
                            # print("lmao")
                            pygame.draw.line(screen, depths[0][1], (x_start, i), (x, i), 1)
                            continue
                    color = depths[0][1]
                    # pygame.draw.line(screen, depths[0][1], (x, i), (x, i), 1)
                    pygame.draw.circle(screen, color, (x, i), 1)
                    # if i == 300 and x == 700:
                        # print(depths)
                        # pygame.draw.circle(screen, (253, 255, 255), (700, 450), 1)
                # pygame.draw.line(screen, (255,255,255), (x0, i), (x1, i), 1)

            # pygame.draw.line(screen, colors[at[j][8]], (x0, i), (x1, i), 1)
            

def construct_edge_table(faces, projected_points, points, width, height):
    # [ yMax, yMin, x, sign, dX, dY, a, b, id ]
    edges = []
    # [ A, B, C, D, (r, g, b), xMax, xMin, z (if C == 0) ]
    polygons = []
    id = 0
    for face in faces:
        # we assume there are 4
        point0 = projected_points[face[0]]
        point1 = projected_points[face[1]]
        point2 = projected_points[face[2]]
        point3 = projected_points[face[3]]
        
        edges.append(construct_edge(point0, point1, width, height, id))
        edges.append(construct_edge(point1, point2, width, height, id))
        edges.append(construct_edge(point2, point3, width, height, id))
        edges.append(construct_edge(point3, point0, width, height, id))
        
        p0 = points[face[0]]
        p1 = points[face[1]]
        p2 = points[face[2]]
        # plane_eq = construct_plane_eq(p0[0]/p0[3], p0[1]/p0[3], p0[2]/p0[3], p1[0]/p1[3], p1[1]/p1[3], p1[2]/p1[3], p2[0]/p2[3], p2[1]/p2[3], p2[2]/p2[3])
        plane_eq = construct_plane_eq(point0[0], point0[1], point0[2], point1[0], point1[1], point1[2], point2[0], point2[1], point2[2])
        
        polygons.append(plane_eq + [(face[4], face[5], face[6]), 0, 0, point0[2] if plane_eq[2] == 0 else 0])
        id += 1
        
    return edges, polygons


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


def construct_plane_eq(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    vector1 = [x2 - x1, y2 - y1, z2 - z1]
    vector2 = [x3 - x1, y3 - y1, z3 - z1]

    cross_product = [vector1[1] * vector2[2] - vector1[2] * vector2[1], -1 * (vector1[0] * vector2[2] - vector1[2] * vector2[0]), vector1[0] * vector2[1] - vector1[1] * vector2[0]]

    a = cross_product[0]
    b = cross_product[1]
    c = cross_product[2]
    d = - (cross_product[0] * x1 + cross_product[1] * y1 + cross_product[2] * z1)
    return [a, b, c, d]
    # a1 = x2 - x1
    # b1 = y2 - y1
    # c1 = z2 - z1
    # a2 = x3 - x1
    # b2 = y3 - y1
    # c2 = z3 - z1
    # a = b1 * c2 - b2 * c1
    # b = a2 * c1 - a1 * c2
    # c = a1 * b2 - b1 * a2
    # d = (- a * x1 - b * y1 - c * z1)
    # return [float(a), float(b), float(c), float(d)]
