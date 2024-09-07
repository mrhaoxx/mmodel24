from core import loong, check_collision
import math


lo = loong(pitch=55, r_turning_space=0)

import pygame
pygame.init()

WINDOW_WIDTH=600
WINDOW_HEIGHT=450

SCALE_WIDTH = 4 * WINDOW_WIDTH
SCALE_HEIGHT = 4 * WINDOW_HEIGHT

screen = pygame.display.set_mode((WINDOW_WIDTH*2, WINDOW_HEIGHT*2))
fake_screen = pygame.Surface((SCALE_WIDTH, SCALE_HEIGHT))
fake_screen.fill((255, 255, 255))

clock = pygame.time.Clock()
GAME_FONT = pygame.freetype.SysFont("consolas", 24)
GAME_FONT_SMALL = pygame.freetype.SysFont("consolas", 20)

center = (SCALE_WIDTH / 2, SCALE_HEIGHT / 2)


def move_point(point, dx, dy):
    return (point[0] + dx, point[1] + dy)

def mirrory_point(point):
    return (point[0], -point[1])

def move_points(points, dx, dy):
    return [(point[0] + dx, point[1] + dy) for point in points]

def mirrory_points(points):
    return [(point[0], -point[1]) for point in points]


def tp(pt):
    return move_point(mirrory_point(pt), center[0], center[1])

def tps(pts):
    return move_points(mirrory_points(pts), center[0], center[1])

iter = 0

paused = False
running = True

speed = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            paused = not paused
            
    if paused:
        clock.tick(60)
        continue
    
    fake_screen.fill((255, 255, 255))
    
    points = lo.get_looong(speed * iter, cutting=3 * math.pi)
    
    corners = []
    inner_lines = []
    
    for pts in points:
        pygame.draw.circle(fake_screen, (0, 0, 0), tp(pts), 5)
        
    for i in range(len(points) - 1):
        pygame.draw.line(fake_screen, (0, 0, 0), tp(points[i]), tp(points[i+1]), 2)
        this_pt = points[i]
        next_pt = points[i + 1]
        
        pts = lo.get_board_points(this_pt, next_pt)
        pygame.draw.lines(fake_screen, (128, 128, 128), True, tps(pts), 1)
        
        
        if i > 4:
            inner_lines.append((pts[1], pts[2]))
            pygame.draw.line(fake_screen, (205, 86, 63), tp(pts[1]), tp(pts[2]), 2)
            
        if i <= 4:
            cor = (pts[1], pts[0], pts[3])
            corners.append(cor)
            for pt in cor:
                pygame.draw.circle(fake_screen, (0, 0, 255), tp(pt), 5)

        for pt in pts:
            pygame.draw.circle(fake_screen, (255, 0, 0),tp(pt), 3)
    
    
    for corner in corners:
        tf, pts = check_collision(corner, inner_lines)
        
        if tf:
            paused = True
            for pt in pts:
                pygame.draw.circle(fake_screen, (0, 255, 0), tp(pt), 10)
            
  
    
    GAME_FONT.render_to(fake_screen, (10, 10), f"ITER: {iter}", (0, 0, 0))
    GAME_FONT.render_to(fake_screen, (10, 30), f"FPS: {clock.get_fps()}", (0, 0, 0))
    GAME_FONT.render_to(fake_screen, (10, 60), f"POINTS: {len(points)}", (0, 0, 0))


    screen.blit(pygame.transform.smoothscale(fake_screen, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
    
    iter += 1
    
pygame.quit()    
            