from utils import point_to_segment_distance, get_distance

from core import loong, check_collision

import math


def check_pitch(pitch):
    l = loong(pitch=pitch, r_turning_space=0)

    speed = 100

    time = 0

    min_step = 1e-6

    max_step = 1e-1

    cur_step = max_step

    max_dist = 20

    r_turning_space = 450

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
                print(f"Pitch {pitch} Collision {time}")
                return False
                
            for ln in inner_lines:
                dist = point_to_segment_distance(corner[1], ln[0], ln[1])
                
                if min_dist is None:
                    min_dist = dist
                else:
                    min_dist = min(min_dist, dist)
                            
        trans_to_step(min_dist)
        
        center_Dis = get_distance(points[0], (0,0))
            
        if center_Dis <= r_turning_space:
            print(f"Pitch {pitch} Center Intersect {time}")
            return True

        time += cur_step


min_pitch = 40

max_pitch = 55

while max_pitch - min_pitch > 1e-8:
    pitch = (min_pitch + max_pitch) / 2

    if check_pitch(pitch):
        max_pitch = pitch
    else:
        min_pitch = pitch
        
    print(f"max {max_pitch} min {min_pitch} delta {max_pitch - min_pitch}")

print(f"Min Pitch: {pitch}")

