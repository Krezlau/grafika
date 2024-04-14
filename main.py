import pygame

from actions import translate, rotate
from projection import WIDTH, HEIGHT, transformation_matrix, BLACK, project, clip_lines, draw_boundaries, init
from scene_parser import parse

pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

(points, connections) = parse('scene1.obj')
print(points)

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

angle = 0.025
fov = 90

# DEBUG = True
DEBUG = False

init(DEBUG)

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
    if keys[pygame.K_x]:
        if fov > 1:
            fov -= 1
        
    tm = transformation_matrix(fov)
    screen.fill(BLACK)

    (projected_points, codes) = project(points, tm)
    clip_lines(projected_points, codes, connections, screen)
    if DEBUG:
        draw_boundaries(screen)
    pygame.display.update()
    