from utils import get_distance

from core import loong, get_speed

time = 0

speed = 100

l = loong(pitch=170,  r_turning_space=450)

def print_speed(speed):
    for s in speed:
        print(f"{s/100:.6f}", end=",")
    print()


time = (l.total_length - l.curved_distance(l.intersect_theta_in)) / speed

time -= 100
delta  = 0

while delta <= 200:
    _speed = get_speed(l, time, speed)
    print_speed(_speed)
    
    time += 1
    delta += 1
    
    





