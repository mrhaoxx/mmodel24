from utils import get_distance

from core import loong, get_speed

time = 0

speed = 100

l = loong(pitch=170,  r_turning_space=450)


time = (l.total_length - l.curved_distance(l.intersect_theta_in)) / speed

time -= 100
delta  = 0

while delta <= 200:
    points = l.get_looong(speed * time)
    for pt in points:
        print(f"{pt[0]/100:.6f},{pt[1]/100:.6f}", end=",")
    print()
    
    time += 1
    delta += 1
    
    





