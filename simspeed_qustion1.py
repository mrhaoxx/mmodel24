from utils import get_distance

from core import loong, get_speed

time = 0

l = loong(pitch=55)

def print_speed(speed):
    for s in speed:
        print(f"{s/100:.6f}", end=",")
    print()

while time <= 300:
    speed = get_speed(l, time, 100)
    print_speed(speed)
    time += 1
    
    





