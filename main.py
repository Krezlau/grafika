import pygame
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

transformation_matrix = np.matrix([
    [1/((WIDTH/HEIGHT) * tan(45)), 0, 0, 0],
    [0, 1/tan(45), 0, 0],
    [0, 0, f/(f-n), -f*n/(f-n)],
    [0, 0, 1, 0]
])


def project(points_to_project):
    projected_points = []
    for point in points_to_project:
        
        if point[2, 0] < 0:
            projected_points.append(np.matrix([-1, -1, -1, -1]).reshape((4, 1)))
        else:
            projected_points.append(np.dot(transformation_matrix, point))
            
    return projected_points

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

    screen.fill(BLACK)
    
    # project
    projected_points = project(points)
    # print(projected_points)
    
    # draw
    for i in range(len(projected_points)):
        x = (projected_points[i][0, 0])/projected_points[i][3, 0] * WIDTH + WIDTH/2
        y = (projected_points[i][1, 0])/projected_points[i][3, 0] * HEIGHT + HEIGHT/2
        # screen.blit(pygame.font.SysFont('Arial', 24).render(str(i), True, WHITE), (x, y))
        pygame.draw.circle(screen, RED, (x, y), 1)
        for connection in connections[i]:
            x2 = (projected_points[connection][0, 0])/projected_points[connection][3, 0] * WIDTH + WIDTH/2
            y2 = (projected_points[connection][1, 0])/projected_points[connection][3, 0] * HEIGHT + HEIGHT/2
            pygame.draw.line(screen, WHITE, (x, y), (x2, y2), 2)
    
    pygame.display.update()
    