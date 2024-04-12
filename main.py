﻿import pygame
import numpy as np
from math import *

from actions import translate, rotate
from scene_parser import parse

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 1280, 720
scale = 50
angle = 0.025

pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

n = 0
f = 1

global fov
global transformation_matrix

fov = 90
transformation_matrix = np.matrix([
    [1/((WIDTH/HEIGHT) * tan(radians(fov)/2)), 0, 0, 0],
    [0, 1/(tan(radians(fov)/2)), 0, 0],
    [0, 0, f/(f-n), -f*n/(f-n)],
    [0, 0, 1, 0]
])


INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8
xmin = 0
xmax = 1
ymin = 0
ymax = 1


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
    return code

def draw(points, codes):
    for i in range(len(points)):
        for connection in connections[i]:
            # both points are outside the screen
            if codes[i] & codes[connection] != 0:
                continue
            if not (codes[i] | codes[connection]):
                pygame.draw.line(screen, WHITE, (points[i][0] * WIDTH + WIDTH/2, points[i][1] * HEIGHT + HEIGHT/2), (points[connection][0] * WIDTH + WIDTH/2, points[connection][1] * HEIGHT + HEIGHT/2))
            else:
                x0 = points[i][0]
                y0 = points[i][1]
                x1 = points[connection][0]
                y1 = points[connection][1]
                
                if codes[i] > codes[connection]:
                    code = codes[i]
                else:
                    code = codes[connection]
                
                if code & TOP:
                    x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                    y = ymax
                    pygame.draw.line(screen, WHITE, (x0 * WIDTH + WIDTH/2, y0 * HEIGHT + HEIGHT/2), (x * WIDTH + WIDTH/2, y * HEIGHT + HEIGHT/2))
                elif code & BOTTOM:
                    x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                    y = ymin
                    pygame.draw.line(screen, WHITE, (x0 * WIDTH + WIDTH/2, y0 * HEIGHT + HEIGHT/2), (x * WIDTH + WIDTH/2, y * HEIGHT + HEIGHT/2))
                elif code & RIGHT:
                    y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                    x = xmax
                    pygame.draw.line(screen, WHITE, (x0 * WIDTH + WIDTH/2, y0 * HEIGHT + HEIGHT/2), (x * WIDTH + WIDTH/2, y * HEIGHT + HEIGHT/2))
                elif code & LEFT:
                    y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                    x = xmin
                    pygame.draw.line(screen, WHITE, (x0 * WIDTH + WIDTH/2, y0 * HEIGHT + HEIGHT/2), (x * WIDTH + WIDTH/2, y * HEIGHT + HEIGHT/2))
                

def project(points_to_project):
    projected_points = []
    codes = []
    for point in points_to_project:
        
        # if point[2, 0] < 0:
        #     projected_points.append(np.matrix([-1, -1, -1, -1]).reshape((4, 1)))
        # else:
        #     projected_points.append(np.dot(transformation_matrix, point))
        
        projection = np.dot(transformation_matrix, point)
        projected_points.append([projection[0, 0] / projection[3, 0], projection[0, 0] / projection[3, 0]])
        codes.append(determine_code(projected_points[-1]))
    return (projected_points, codes)

(points, connections) = parse('scene1.obj')
print(points)

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

clock = pygame.time.Clock()
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        points = translate(-0.1, 0, 0, points)
    if keys[pygame.K_a]:
        points = translate(0.1, 0, 0, points)
    if keys[pygame.K_w]:
        points = translate(0, 0, -0.1, points)
    if keys[pygame.K_s]:
        points = translate(0, 0, 0.1, points)
    if keys[pygame.K_LSHIFT]:
        points = translate(0, -0.1, 0, points)
    if keys[pygame.K_SPACE]:
        points = translate(0, 0.1, 0, points)
    if keys[pygame.K_LEFT]:
        points = rotate(angle, 'y', points)
    if keys[pygame.K_RIGHT]:
        points = rotate(-angle, 'y', points)
    if keys[pygame.K_UP]:
        points = rotate(-angle, 'x', points)
    if keys[pygame.K_DOWN]:
        points = rotate(angle, 'x', points)
    if keys[pygame.K_q]:
        points = rotate(angle, 'z', points)
    if keys[pygame.K_e]:
        points = rotate(-angle, 'z', points)
    if keys[pygame.K_z]:
        if fov < 179:
            fov += 1
        transformation_matrix = np.matrix([
            [1/((WIDTH/HEIGHT) * tan(radians(fov)/2)), 0, 0, 0],
            [0, 1/(tan(radians(fov)/2)), 0, 0],
            [0, 0, f/(f-n), -f*n/(f-n)],
            [0, 0, 1, 0]
        ])
    if keys[pygame.K_x]:
        if (fov > 1):
            fov -= 1
        transformation_matrix = np.matrix([
            [1/((WIDTH/HEIGHT) * tan(radians(fov)/2)), 0, 0, 0],
            [0, 1/(tan(radians(fov)/2)), 0, 0],
            [0, 0, f/(f-n), -f*n/(f-n)],
            [0, 0, 1, 0]
        ]) 
        

    screen.fill(BLACK)
    
    # project
    (projected_points, codes) = project(points)
    # print(projected_points)
    # print(transformation_matrix)
    print(fov)
    draw(projected_points, codes)
    
    # draw
    # for i in range(len(projected_points)):
    #     x = (projected_points[i][0, 0])/projected_points[i][3, 0] * WIDTH + WIDTH/2
    #     y = (projected_points[i][1, 0])/projected_points[i][3, 0] * HEIGHT + HEIGHT/2
    #     # screen.blit(pygame.font.SysFont('Arial', 24).render(str(i), True, WHITE), (x, y))
    #     # pygame.draw.circle(screen, RED, (x, y), 1)
    #     for connection in connections[i]:
    #         x2 = (projected_points[connection][0, 0])/projected_points[connection][3, 0] * WIDTH + WIDTH/2
    #         y2 = (projected_points[connection][1, 0])/projected_points[connection][3, 0] * HEIGHT + HEIGHT/2
    #         pygame.draw.line(screen, WHITE, (x, y), (x2, y2), 2)


    pygame.display.update()