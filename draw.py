from core import loong


lo = loong(pitch=55)

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

iter = 0

paused = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            paused = not paused
    
    fake_screen.fill((255, 255, 255))
    
    points = lo.get_looong(iter)
    
    for pts in points:
        pygame.draw.circle(fake_screen, (0, 0, 0), move_point(mirrory_point(pts), center[0], center[1]), 5)
        
    for i in range(len(points) - 1):
        pygame.draw.line(fake_screen, (0, 0, 0), move_point(mirrory_point(points[i]), center[0], center[1]), move_point(mirrory_point(points[i+1]), center[0], center[1]), 2)
        if i < len(points) - 1:
            this_pt = points[i]
            next_pt = points[i + 1]
            
            pts = lo.get_board_points(this_pt, next_pt)
            pygame.draw.lines(fake_screen, (128, 128, 128), True, move_points(mirrory_points(pts), center[0], center[1]), 1)

            for pt in pts:
                pygame.draw.circle(fake_screen, (255, 0, 0), move_point(mirrory_point(pt), center[0], center[1]), 3)
        
    
    
    
    GAME_FONT.render_to(fake_screen, (10, 30), "FPS: " + str(clock.get_fps()), (0, 0, 0))
    GAME_FONT.render_to(fake_screen, (10, 60), f"POINTS: {len(points)}", (0, 0, 0))

    screen.blit(pygame.transform.smoothscale(fake_screen, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()
    
    iter += 1
    
pygame.quit()    
            