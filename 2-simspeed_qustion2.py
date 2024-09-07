from utils import get_distance

from core import loong, get_speed

time = 412.4738380504162

l = loong(pitch=55, r_turning_space=0)

def print_speed(speed):
    for s in speed:
        print(f"{s/100:.6f}", end=",")
    print()

speed = get_speed(l, time, 100)

print_speed(speed)







