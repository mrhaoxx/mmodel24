from utils import get_distance

from core import loong



def get_ptr_speeds(points_before, points_after, interval):
    speeds = []
    for i in range(len(points_before)):
        distance = get_distance(points_before[i], points_after[i])
        speeds.append(distance / interval)
    return speeds

def get_speed(l: loong, time, speed, interval = 1e-4):
    points_before = l.get_looong((time - interval) * speed) 
    points_after = l.get_looong((time + interval) * speed)
    return get_ptr_speeds(points_before, points_after, 2 * interval)

time = 1

l = loong(pitch=55)

def print_speed(speed):
    for s in speed:
        print(f"{s:.6f}", end=",")
    print()

while time <= 300:
    speed = get_speed(l, time, 100)
    print_speed(speed)
    time += 1
    
    





