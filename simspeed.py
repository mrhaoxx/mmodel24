from utils import get_distance

from core import get_looong

def get_ptr_speeds(points_before, points_after, interval):
    speeds = []
    for i in range(len(points_before)):
        distance = get_distance(points_before[i], points_after[i])
        speeds.append(distance / interval)
    return speeds

def get_speed(time, speed, interval = 1e-7):
    points_before = get_looong(time * speed) 
    points_after = get_looong((time + interval) * speed)
    return get_ptr_speeds(points_before, points_after, interval)

import pygame
clock = pygame.time.Clock()

while True:

    speed = get_speed(1342.84, 100)
    clock.tick()
    print(clock.get_fps())





