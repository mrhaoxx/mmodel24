from utils import get_distance

from core import loong, get_speed

from speed_formula import compute_v_next

import sys

time = float(sys.argv[1])

l = loong(pitch=55, r_turning_space=0)

def print_speed(speed):
    for s in speed:
        print(f"{s/100:.6f}", end=",")
    print()

speed = get_speed(l, time, 100)

points = l.get_looong(100 * time, return_theta=True)

speed_ = 100

speed_for = []

for i in range(len(points[1]) - 1):
    speed_for.append(speed_)
    speed_ = compute_v_next(speed_, l.b, l.board_length_head if i == 0 else l.board_length, points[1][i] , points[1][i+1])
    
speed_for.append(speed_)

# print(len(speed_for), len(speed))
# for i in range(len(speed_for)):
#     print(speed_for[i] - speed[i], end=",")
#     print(speed_for[i], end=",")

print_speed(speed_for)


