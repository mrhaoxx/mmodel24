from utils import get_distance

from core import loong, get_speed

time = 412.47383774746515
speed = 100

l = loong(pitch=55, r_turning_space=0)

points = l.get_looong(speed * time)
for pt in points:
    print(f"{pt[0]/100:.6f},{pt[1]/100:.6f}", end=",")
print()




