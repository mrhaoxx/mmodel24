import pygame
import math
import csv

import numpy as np
from scipy.integrate import quad
from scipy.optimize import *

from utils import *

pygame.init()

WINDOW_WIDTH=600
WINDOW_HEIGHT=450

SCALE_WIDTH = 3 * WINDOW_WIDTH
SCALE_HEIGHT = 3 * WINDOW_HEIGHT

screen = pygame.display.set_mode((WINDOW_WIDTH*2, WINDOW_HEIGHT*2))
fake_screen = pygame.Surface((SCALE_WIDTH, SCALE_HEIGHT))

fake_screen.fill((255, 255, 255))

clock = pygame.time.Clock()
GAME_FONT = pygame.freetype.SysFont("consolas", 24)
GAME_FONT_SMALL = pygame.freetype.SysFont("consolas", 20)

center = (SCALE_WIDTH / 2, SCALE_HEIGHT / 2)

a = 0
b = 170 / (2 * math.pi)
theta_max = 32 * math.pi 

board_outer_width = 27.5
board_width = 30.

board_length_head = 341 - 55
board_length = 220 - 55

r_tuning_space = 450

nodenum = 222


time = 0
delta_t = 0.01

speed = 100

board_alpha = math.atan2(board_outer_width, (board_width / 2))
board_slash = math.sqrt(pow(board_outer_width, 2) + pow(board_width / 2, 2))
board_beta = 2*math.atan2(board_width / 2, board_outer_width)

def get_board_points(pt1, pt2):
    theta = math.atan2((pt1[1] - pt2[1]),(pt2[0] - pt1[0]))
    alpha = math.pi / 2 - theta - board_alpha
    
    d1 = (board_slash * math.cos(alpha))
    d2 = (board_slash * math.sin(alpha))
    
    sigma = (math.pi / 2 ) - board_beta + alpha
    
    d3 = board_slash * math.cos(sigma)
    d4 = board_slash * math.sin(sigma)
    
    x1 = pt1[0] - d1
    y1 = pt1[1] - d2
    
    x2 = pt1[0] - d4
    y2 = pt1[1] + d3
    
    x3 = pt2[0] + d1
    y3 = pt2[1] + d2
    
    x4 = pt2[0] + d4
    y4 = pt2[1] - d3
    
    return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

# 反查点
points = []
point_s = []
point_theta = []
point_turning_space = []


def get_point_in(theta):
    r = a + b * theta
    x = center[0] + r * math.cos(theta)
    y = center[1] + r * math.sin(theta)
    return x, y

def get_point_out(theta):
    r = a + b * theta
    x = center[0] - r * math.cos(-theta)
    y = center[1] + r * math.sin(-theta)
    return x, y


def get_point_direction_in(theta):
    r = a + b * theta
    return math.atan2(r * math.cos(theta) + math.sin(theta) * b,- r * math.sin(theta) + b * math.cos(theta))


def get_point_direction_out(theta):
    r = a + b * theta
    return math.atan2(- r * math.cos(theta) - math.sin(theta) * b, r * math.sin(theta) - b * math.cos(theta))


# def get_point_distance(theta, sp = 0):
#     length, _ = quad(arc_length, sp, theta)
#     return length 



theta = 0
while theta <= math.pi * 2:
    x = center[0] +  r_tuning_space * math.cos(theta)
    y = center[1] +  r_tuning_space * math.sin(theta)
    point_turning_space.append((x, y))
    theta += 0.01


paused = False


def eq_intersect_in_track(theta, target_dis, curve):
    return get_distance(curve(theta), center) - target_dis

intersect_theta_in = newton(eq_intersect_in_track, 0, args=(r_tuning_space,get_point_in))
intersect_theta_in_direction_theta = get_point_direction_in(intersect_theta_in)
intersect_theta_in_direction_theta_cross = intersect_theta_in_direction_theta + math.pi / 2
intersect_in = get_point_in(intersect_theta_in)
intersect_in_start = (intersect_in[0] - 100 * math.cos(intersect_theta_in_direction_theta), intersect_in[1] - 100 * math.sin(intersect_theta_in_direction_theta))
intersect_in_end = (intersect_in[0] + 100 * math.cos(intersect_theta_in_direction_theta), intersect_in[1] + 100 * math.sin(intersect_theta_in_direction_theta))
intersect_in_cross_start = (intersect_in[0] - 1000 * math.cos(intersect_theta_in_direction_theta_cross), intersect_in[1] - 1000 * math.sin(intersect_theta_in_direction_theta_cross))
intersect_in_cross_end = (intersect_in[0] + 1000 * math.cos(intersect_theta_in_direction_theta_cross), intersect_in[1] + 1000 * math.sin(intersect_theta_in_direction_theta_cross))

intersect_theta_out = newton(eq_intersect_in_track, 0, args=(r_tuning_space,get_point_out))
intersect_theta_out_direction_theta = get_point_direction_out(intersect_theta_out)
intersect_theta_out_direction_theta_cross = intersect_theta_out_direction_theta + math.pi / 2

intersect_out = get_point_out(intersect_theta_out)
intersect_out_start = (intersect_out[0] - 100 * math.cos(intersect_theta_out_direction_theta), intersect_out[1] - 100 * math.sin(intersect_theta_out_direction_theta))
intersect_out_end = (intersect_out[0] + 100 * math.cos(intersect_theta_out_direction_theta), intersect_out[1] + 100 * math.sin(intersect_theta_out_direction_theta))
intersect_out_cross_start = (intersect_out[0] - 1000 * math.cos(intersect_theta_out_direction_theta_cross), intersect_out[1] - 1000 * math.sin(intersect_theta_out_direction_theta_cross))
intersect_out_cross_end = (intersect_out[0] + 1000 * math.cos(intersect_theta_out_direction_theta_cross), intersect_out[1] + 1000 * math.sin(intersect_theta_out_direction_theta_cross))


ipx_p_in = get_intersection_point(intersect_in_start, intersect_in_end, intersect_out_cross_end, intersect_out_cross_start)
ipx_p_out = get_intersection_point(intersect_out_start, intersect_out_end, intersect_in_cross_end, intersect_in_cross_start)

o_w = get_distance(ipx_p_out, intersect_out)
o_l = get_distance(ipx_p_in, intersect_out)

print(intersect_theta_in)
print(intersect_theta_out)

phi = math.atan(1/intersect_theta_in)

o_r = r_tuning_space / (3 * math.cos(phi))
print(o_r, o_w, o_l)

rate_1 = 2 * o_r / o_l
rate_2 = o_r / o_l

o_point_1 = (intersect_in[0] * (1 - rate_1) + ipx_p_out[0] * rate_1, intersect_in[1] * (1 - rate_1) + ipx_p_out[1] * rate_1)
o_point_2 = (intersect_out[0] * (1 - rate_2) + ipx_p_in[0] * rate_2, intersect_out[1] * (1 - rate_2) + ipx_p_in[1] * rate_2)

o_beta = (math.pi - math.asin(o_w / (3 * o_r)))

o_point1_circle_points = []
o_point2_circle_points = []

theta = 0
while theta <= 2 * math.pi:
    x = o_point_1[0] + 2 * o_r * math.cos(theta)
    y = o_point_1[1] + 2 * o_r * math.sin(theta)
    o_point1_circle_points.append((x, y))
    theta += 0.01
    
theta = 0
while theta <= math.pi * 2:
    x = o_point_2[0] + o_r * math.cos(theta)
    y = o_point_2[1] + o_r * math.sin(theta)
    o_point2_circle_points.append((x, y))
    theta += 0.01

def get_point_posR(theta):
    x = o_point_1[0] + 2 * o_r * math.cos(theta)
    y = o_point_1[1] + 2 * o_r * math.sin(theta)
    return x, y
    
def get_point_negR(theta):
    x = o_point_2[0] + o_r * math.cos(theta)
    y = o_point_2[1] + o_r * math.sin(theta)
    return x, y

def curved(theta):
    if theta > intersect_theta_in:
        return get_point_in(theta)
    elif theta < -intersect_theta_out:
        return get_point_out(-theta)
    elif theta > 0:
        return get_point_posR(theta * (o_beta / intersect_theta_in) +  intersect_theta_in +  math.pi + (math.pi - o_beta) / 2)
    else:
        return get_point_negR(-theta * (o_beta / intersect_theta_out) + intersect_theta_out  + (math.pi - o_beta) / 2)

o_circum_1 = o_beta * 2 * o_r
o_circum_2 = o_beta * o_r


c_bsquared2 = b / 2
c_sp = c_bsquared2 * (intersect_theta_in * math.sqrt(1 + intersect_theta_in * intersect_theta_in) + math.log(intersect_theta_in + math.sqrt(1 + intersect_theta_in * intersect_theta_in)))

def get_point_distance(theta, sp = 0):
    return c_bsquared2 * (theta * math.sqrt(1 + theta * theta) + math.log(theta + math.sqrt(1 + theta * theta))) - c_sp
    

def curved_distance(theta):
    if theta > intersect_theta_in:
        return get_point_distance(theta, sp = intersect_theta_in) + o_circum_1
    elif theta < -intersect_theta_out:
        return - get_point_distance(-theta, sp = intersect_theta_out) - o_circum_2
    elif theta > 0:
        return theta * (o_beta / intersect_theta_in) * 2 * o_r
    else:
        return theta * (o_beta / intersect_theta_out) * o_r


# 生成螺线的点
theta =  - theta_max
while theta <= theta_max:
    points.append(curved(theta))
    point_s.append(curved_distance(theta))
    
    point_theta.append(theta)
    theta += 0.1 

cur_point_idx = len(points) - 2

total_length = point_s[-1]

last_point_distance = []

for i in range(nodenum + 1):
    last_point_distance.append(point_s[-1])
    

def eq_head_point(theta, lambda1):
    return curved_distance(theta) - lambda1
    
def get_head_point(el_s):
    global cur_point_idx
    
    r_length = total_length - el_s
    
    while (point_s[cur_point_idx] >= r_length):
        if cur_point_idx == 0:
            return points[0], 0
        cur_point_idx -= 1

    theta = newton(eq_head_point, point_theta[cur_point_idx], args=(r_length,))
    return curved(theta), theta

def eq_point_chain_sim(theta2, point1, distance):
    return (get_distance(curved(theta2), point1) - distance)
    

def get_point_chain_next_sim(theta1, point1, distance):
    itec = math.pi / 4
    
    while eq_point_chain_sim(theta1 + itec, point1, distance) <= 0:
        itec += math.pi / 4
        
    theta = root_scalar(eq_point_chain_sim, bracket=[theta1, theta1 + itec], args=(point1, distance), method='brentq')
    
    return theta.root, curved(theta.root)


# print( total_length - curved_distance(intersect_theta_in))

time = (total_length - curved_distance(intersect_theta_in)) / speed

# time -= 100
# time = 1342.5
print(time)
max_spd = {}

for i in range(nodenum + 1):
    max_spd[i] = 0

iter = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            paused = not paused

    if paused:
        clock.tick(60)
        continue
    # screen.fill((255, 255, 255))
    iter += 1
    
    
    fake_screen.fill((255, 255, 255))
    distance = 0
    inner_lines = []
    checking_outer_points = []
    
    if len(points) > 1:
        pygame.draw.lines(fake_screen, (0, 0, 255), False, points, 2)
        
    pygame.draw.lines(fake_screen, (255, 0, 0), False, point_turning_space, 2)
    
    pygame.draw.circle(fake_screen, (0, 0, 0), intersect_in, 5)
    pygame.draw.circle(fake_screen, (0, 0, 0), intersect_out, 5)
    
    pygame.draw.lines(fake_screen, (255, 0, 0), False, [intersect_in_start, intersect_in_end], 2)
    pygame.draw.lines(fake_screen, (255, 0, 0), False, [intersect_in_cross_start, intersect_in_cross_end], 2)
    
    pygame.draw.lines(fake_screen, (0, 0, 0), False, [intersect_out_start, intersect_out_end], 2)
    pygame.draw.lines(fake_screen, (0, 0, 0), False, [intersect_out_cross_start, intersect_out_cross_end], 2)

    pygame.draw.circle(fake_screen, (111, 111, 0), ipx_p_in, 4)
    pygame.draw.circle(fake_screen, (111, 111, 0), ipx_p_out, 4)
    pygame.draw.circle(fake_screen, (0, 0, 0), o_point_1, 8)
    pygame.draw.circle(fake_screen, (0, 0, 0), o_point_2, 8)
    
    pygame.draw.lines(fake_screen, (255, 0, 128), False, o_point1_circle_points, 2)
    pygame.draw.lines(fake_screen, (128, 0, 255), False, o_point2_circle_points, 2)
    
    pygame.draw.circle(fake_screen, (0, 0, 0), center, 5)
    
    # theta = 20
    # while theta >= -20:
    #     pygame.draw.circle(fake_screen, ( abs(255 * (theta / 100)), abs(255 * (theta / 100)), 0), curved(theta), 2 )
    #     theta -= 0.01
        
    # theta = - (time) * 1 + 1
    
    # pygame.draw.circle(fake_screen, ( 255, 0, 0), curved(theta), 10)
    
    # GAME_FONT.render_to(fake_screen, (500, 30), f"THETA:{theta:.3f} DIS: {curved_distance(theta)}", (0, 0, 0))

    current_s = time * speed
    
    head_point, theta1 = get_head_point(current_s)
    
    pygame.draw.circle(fake_screen, (255, 0, 0), head_point, 5)
    
    sec_point_theta = theta1
    sec_point = head_point
    speed_ = speed
    
    # speed__ = speed     
    
    for i in range(nodenum + 1):
        
        # if sec_point_theta - theta1 > 3 * math.pi:
        #     break
        
        if i == 0:
            _sec_point_theta, _sec_point = get_point_chain_next_sim(sec_point_theta, sec_point, board_length_head)
        elif i == nodenum:
            pass
        else:
            _sec_point_theta, _sec_point = get_point_chain_next_sim(sec_point_theta, sec_point, board_length)
            
        if not nodenum == 0:
            pygame.draw.circle(fake_screen, (0, 255 * (i/nodenum), 255 * (i/nodenum)), _sec_point, 3)
        
        _distance = get_distance(sec_point, _sec_point)
        distance += _distance
    
        if not i == nodenum:
            pts = get_board_points(_sec_point, sec_point)
            pygame.draw.lines(fake_screen, (128, 128, 128), True, pts, 3)
        # for pt in pts[0:1]:
        # pygame.draw.circle(fake_screen, (116, 152, 93), pts[0], 4)
        # pygame.draw.circle(fake_screen, (116, 152, 93), pts[3], 4)
        # pygame.draw.line(fake_screen, (0, 0, 0), pts[0], pts[3], 1)
        
        # if i > 3:
        #     inner_lines.append((pts[0], pts[3]))
        
        # if i == 0 or i == 1:
        #     checking_outer_points.append((pts[1], pts[2]))
        #     checking_outer_points.append((pts[1], pts[0]))
        #     checking_outer_points.append((pts[3], pts[2]))
            
        this_dis = curved_distance(sec_point_theta)
        
        speed__ = (this_dis - last_point_distance[i]) / delta_t
        
        if iter > 3:
            max_spd[i] = max(max_spd[i], -speed__)
        
        p_x = sec_point[0] - center[0]
        p_y = - sec_point[1] + center[1]
  

        # if i < 6:
        #     GAME_FONT_SMALL.render_to(fake_screen, (10, 130 + 20 * (i)), f"P_{i:3}: {sec_point_theta:12.5f} {this_dis:12.5f} {p_x:12.5f},{p_y:12.5f} {-speed__:10.5f} {max_spd[i]:20.10f}" , (0, 0, 0))

        
        sec_point = _sec_point
        sec_point_theta = _sec_point_theta
        last_point_distance[i] = this_dis

    GAME_FONT.render_to(fake_screen, (10, 10), f"DIS:  {distance:.6f}", (0, 0, 0))
    GAME_FONT.render_to(fake_screen, (10, 30), "FPS: " + str(clock.get_fps()), (0, 0, 0))
    GAME_FONT.render_to(fake_screen, (10, 50), "TIME: " + str(time), (0, 0, 0))
    
    center_Dis = get_distance(head_point, center)
    
    GAME_FONT.render_to(fake_screen, (10, 80), f"CENTER DIS: {center_Dis}", (255, 0, 0) if center_Dis > r_tuning_space else (0, 255, 0))
        
    # for pt in checking_outer_points:
    #     pygame.draw.lines(fake_screen, (0, 0, 255), False, pt, 2)

    #     P = None
    #     for i in range(len(inner_lines)):
    #         w, P = is_intersecting_with_point(inner_lines[i][0], inner_lines[i][1], pt[0], pt[1])
    #         if w:
    #             HAS_INTERSECT = True
    #             intersection_points.append(P)
    #             break
            
    # if HAS_INTERSECT:
    #     # paused = True
    #     print("Intersect", pt, inner_lines[i], time)
    #     GAME_FONT.render_to(fake_screen, (10, 110), f"Intersect at: {intersection_points}", (255, 0, 0))
    #     for pt in intersection_points:
    #         pygame.draw.circle(fake_screen, (255, 0, 0), pt, 5)
    # else:
    #     GAME_FONT.render_to(fake_screen, (10, 110), f"Not Intersect", (0, 255, 0))

    screen.blit(pygame.transform.smoothscale(fake_screen, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()

    time += delta_t

pygame.quit()