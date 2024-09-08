from utils import point_to_segment_distance

from core import loong, check_collision

import math,sys

l = loong(pitch=55, r_turning_space=0)

speed = 100

time = 0

min_step = 1e-7

max_step = 1e-1

cur_step = max_step

max_dist = 20

def trans_to_step(dist):
    global cur_step
    
    dist = min(max_dist, dist)
    
    cur_step = min_step + (max_step - min_step) * (dist / max_dist)

while True:
    
    points = l.get_looong(speed * time, cutting=3 * math.pi)
    
    corners = []
    inner_lines = []
    
    for i in range(len(points) - 1):
        this_pt = points[i]
        next_pt = points[i + 1]
        
        pts = l.get_board_points(this_pt, next_pt)
        
        if i > 4:
            inner_lines.append((pts[1], pts[2]))
            
        if i <= 4:
            cor = (pts[1], pts[0], pts[3])
            corners.append(cor)


    min_dist = None
    
    for corner in corners:
        tf, pts = check_collision(corner, inner_lines)
        
        if tf:
            print(file=sys.stderr)
            print(time)
            exit(0)
        
        for ln in inner_lines:
            dists = []

            for cr in corner:
                dists.append(point_to_segment_distance(cr, ln[0], ln[1]))
            
            dist = min(dists)

            if min_dist is None:
                min_dist = dist
            else:
                min_dist = min(min_dist, dist)
                
    trans_to_step(min_dist)
    
    time += cur_step

    print(f"+{time:15.6f}s {cur_step:15.9f} {min_dist:15.9f}", end="\r", file=sys.stderr)

