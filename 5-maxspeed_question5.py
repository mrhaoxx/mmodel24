from utils import get_distance

from core import loong, get_speed

time = 0

speed = 124.62666525

l = loong(pitch=170,  r_turning_space=450)


time = (l.total_length - l.curved_distance(l.intersect_theta_in)) / speed


min_step = 1e-7

max_step = 1e-1

cur_step = max_step

max_speed = 200

_max_sped = 0

r_turning_space = 450

def trans_to_step(speed):
    global cur_step
    
    dist = min(max_speed, speed)
    
    cur_step = max_step + (min_step - max_step) * (dist / max_speed)

delta  = 0

while delta <= 100:
    _speed = get_speed(l, time, speed)

    max_sped = max(_speed)
    
    _max_sped = max(_max_sped, max_sped)
    
    trans_to_step(max_sped)
    
    time += cur_step
    delta += cur_step
    
    print(f"+{time:15.6f}s {max_sped/100:15.9f} {_max_sped/100:15.9f} {cur_step:15.9f}", end="\r")
    
    
print()
print(f"Max speed: {_max_sped/100:.6f}")