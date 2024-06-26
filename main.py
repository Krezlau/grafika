﻿import pygame

from actions import translate, rotate
from face_printer import print_faces
from projection import WIDTH, HEIGHT, transformation_matrix, BLACK, project, clip_lines, draw_boundaries, init
from scene_parser import parse

pygame.display.set_caption("grafika")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

(points, connections, faces) = parse('scene1.obj')

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

angle = 0.5
fov = 90

# If DEBUG is True, the screen will be smaller and the boundaries will be drawn
# DEBUG = True
DEBUG = False

# STATICMODE = False
STATICMODE = True
init(DEBUG)

speed = 1

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
            if event.key == pygame.K_m:
                if speed == 1:
                    speed = 2
                else:
                    speed = 1
            if STATICMODE:
                if event.key == pygame.K_d:
                    points = translate(10 * speed * -0.05, 0, 0, points)
                if event.key == pygame.K_a:
                    points = translate(10 * speed * 0.05, 0, 0, points)
                if event.key == pygame.K_w:
                    points = translate(0, 0, 10 * speed * -0.05, points)
                if event.key == pygame.K_s:
                    points = translate(0, 0, 10 * speed * 0.05, points)
                if event.key == pygame.K_LSHIFT:
                    points = translate(0, 10 * speed * -0.05, 0, points)
                if event.key == pygame.K_SPACE:
                    points = translate(0, 10 * speed * 0.05, 0, points)
                if event.key == pygame.K_LEFT:
                    points = rotate(10 * speed * angle, 'y', points)
                if event.key == pygame.K_RIGHT:
                    points = rotate(10 * speed * -angle, 'y', points)
                if event.key == pygame.K_UP:
                    points = rotate(10 * speed * -angle, 'x', points)
                if event.key == pygame.K_DOWN:
                    points = rotate(10 * speed * angle, 'x', points)
                if event.key == pygame.K_q:
                    points = rotate(10 * speed * angle, 'z', points)
                if event.key == pygame.K_e:
                    points = rotate(10 * speed * -angle, 'z', points)
                if event.key == pygame.K_z:
                    if fov < 179:
                        fov += 10
                if event.key == pygame.K_x:
                    if fov > 1:
                        fov -= 10
                
    if not STATICMODE:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            points = translate(speed * -0.05, 0, 0, points)
        if keys[pygame.K_a]:
            points = translate(speed * 0.05, 0, 0, points)
        if keys[pygame.K_w]:
            points = translate(0, 0, speed * -0.05, points)
        if keys[pygame.K_s]:
            points = translate(0, 0, speed * 0.05, points)
        if keys[pygame.K_LSHIFT]:
            points = translate(0, speed * -0.05, 0, points)
        if keys[pygame.K_SPACE]:
            points = translate(0, speed * 0.05, 0, points)
        if keys[pygame.K_LEFT]:
            points = rotate(speed * angle, 'y', points)
        if keys[pygame.K_RIGHT]:
            points = rotate(speed * -angle, 'y', points)
        if keys[pygame.K_UP]:
            points = rotate(speed * -angle, 'x', points)
        if keys[pygame.K_DOWN]:
            points = rotate(speed * angle, 'x', points)
        if keys[pygame.K_q]:
            points = rotate(speed * angle, 'z', points)
        if keys[pygame.K_e]:
            points = rotate(speed * -angle, 'z', points)
        if keys[pygame.K_z]:
            if fov < 179:
                fov += 1
        if keys[pygame.K_x]:
            if fov > 1:
                fov -= 1
        
    tm = transformation_matrix(fov)
    screen.fill(BLACK)

    (projected_points, codes) = project(points, tm)
    # clip_lines(projected_points, codes, connections, screen)
    print_faces(projected_points, points, faces, screen, WIDTH, HEIGHT)
    
    # for i in range(8):
    #     text = my_font.render(str(i), False, (255, 255, 255))
    #     screen.blit(text, (int(projected_points[i][0] * WIDTH + WIDTH/2), int(projected_points[i][1] * HEIGHT + HEIGHT/2)))
    #     pygame.draw.circle(screen, (0, 255, 0), (int(projected_points[i][0] * WIDTH + WIDTH/2), int(projected_points[i][1] * HEIGHT + HEIGHT/2)), 5)
    # 
    if DEBUG:
        draw_boundaries(screen)
    pygame.display.update()
    