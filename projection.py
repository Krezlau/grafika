import pygame
import numpy as np
from math import *

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# codes 
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8
BEHIND = 16
FRONT = 32

global xmin, xmax, ymin, ymax, zmin, zmax
WIDTH = 1280
HEIGHT = 720


def init(DEBUG):
    global xmin, xmax, ymin, ymax, zmin, zmax
    if DEBUG:
        xmin = -0.25
        xmax = 0.25
        ymin = -0.25
        ymax = 0.25
        zmin = 0
        zmax = 1000
    else:
        xmin = -0.5
        xmax = 0.5
        ymin = -0.5
        ymax = 0.5
        zmin = 0
        zmax = 1000


# transformation matrix
n = 0
f = 1000
def transformation_matrix(fov):
    return np.matrix([
        [1/((WIDTH/HEIGHT) * tan(radians(fov)/2)), 0, 0, 0],
        [0, 1/(tan(radians(fov)/2)), 0, 0],
        [0, 0, f/(f-n), -f*n/(f-n)],
        [0, 0, 1, 0]
    ])



def determine_code(point):
    code = INSIDE
    if point[0] < xmin:
        code |= LEFT
    elif point[0] > xmax:
        code |= RIGHT
    if point[1] < ymin:
        code |= BOTTOM
    elif point[1] > ymax:
        code |= TOP
    if point[2] < zmin:
        code |= BEHIND
    elif point[2] > zmax:
        code |= FRONT
    return code


def clip_lines(points, codes, connections, screen):
    for i in range(len(points)):
        for connection in connections[i]:
            # both points are outside the screen
            if codes[i] & codes[connection] != 0:
                continue
            if not (codes[i] | codes[connection]):
                draw(points[i][0], points[i][1], points[connection][0], points[connection][1], screen)
            else:
                x0, y0 = clip_points(codes[i], points[i][0], points[i][1], points[i][2], points[connection][0], points[connection][1], points[connection][2])
                x1, y1 = clip_points(codes[connection], points[connection][0], points[connection][1], points[connection][2], points[i][0], points[i][1], points[i][2])
                if x0 is not None and x1 is not None and y0 is not None and y1 is not None:
                    draw(x0, y0, x1, y1, screen)
                # if x0 is not None and y0 is not None:
                #     draw(x0, y0, points[connection][0], points[connection][1], screen)



def clip_points(code, x0, y0, z0, x1, y1, z1):
    x = None
    y = None
    if code == INSIDE:
        return x0, y0
    
    if code & FRONT:
        return x, y
    elif code & BEHIND:
        if round(z1, 4) == 0:
            return x, y
        x = x0 + (x1 - x0) * (zmax - z0) / (z1 - z0)
        y = y0 + (y1 - y0) * (zmax - z0) / (z1 - z0)
        print(x, y)
    elif code & TOP:
        x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
        y = ymax
    elif code & BOTTOM:
        x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
        y = ymin
    elif code & RIGHT:
        y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
        x = xmax
    elif code & LEFT:
        y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
        x = xmin
        
    return x, y


def draw(x0, y0, x1, y1, screen):
    X0 = x0 * WIDTH + WIDTH/2
    Y0 = y0 * HEIGHT + HEIGHT/2
    X1 = x1 * WIDTH + WIDTH/2
    Y1 = y1 * HEIGHT + HEIGHT/2
    pygame.draw.line(screen, WHITE, (X0, Y0), (X1, Y1), 2)


def project(points_to_project, tm):
    projected_points = []
    codes = []
    for point in points_to_project:

        projection = np.dot(tm, point)
        projected_points.append([projection[0, 0]/projection[3,0], projection[1, 0]/projection[3,0], point[2, 0], projection[3, 0]])
        codes.append(determine_code(projected_points[-1]))

    return projected_points, codes


def draw_boundaries(screen):
    pygame.draw.line(screen, RED, (xmin*WIDTH+WIDTH/2, ymin*HEIGHT+HEIGHT/2), (xmax*WIDTH+WIDTH/2, ymin*HEIGHT+HEIGHT/2), 2)
    pygame.draw.line(screen, RED, (xmin*WIDTH+WIDTH/2, ymax*HEIGHT+HEIGHT/2), (xmax*WIDTH+WIDTH/2, ymax*HEIGHT+HEIGHT/2), 2)
    pygame.draw.line(screen, RED, (xmax*WIDTH+WIDTH/2, ymax*HEIGHT+HEIGHT/2), (xmax*WIDTH+WIDTH/2, ymin*HEIGHT+HEIGHT/2), 2)
    pygame.draw.line(screen, RED, (xmin*WIDTH+WIDTH/2, ymin*HEIGHT+HEIGHT/2), (xmin*WIDTH+WIDTH/2, ymax*HEIGHT+HEIGHT/2), 2)