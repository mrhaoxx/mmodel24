import pygame
import math
import csv

import numpy as np
from scipy.integrate import quad
from scipy.optimize import *

pygame.init()

WINDOW_WIDTH=600
WINDOW_HEIGHT=450

SCALE_WIDTH = 4 * WINDOW_WIDTH
SCALE_HEIGHT = 4 * WINDOW_HEIGHT

screen =  pygame.display.set_mode((WINDOW_WIDTH*2, WINDOW_HEIGHT*2))
fake_screen = pygame.Surface((SCALE_WIDTH, SCALE_HEIGHT))

fake_screen.fill((255, 255, 255))

clock = pygame.time.Clock()
GAME_FONT = pygame.freetype.SysFont("consolas", 24)

# 圆心位置
center = (SCALE_WIDTH / 2, SCALE_HEIGHT / 2)


# 等距螺线参数
a = 0 * math.pi  # 起始半径
b = 170 / (2 * math.pi)
theta_max = 32 * math.pi 

board_outer_width = 027.5
board_width = 30.

board_length_head = 341 - 55
board_length = 220 - 55

time = 0
delta_t = 0.01

nodenum = 223
speed = 100


r_tuning_space = 450

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
    
def cross_product(p1, p2, p3):
    """计算向量 p1p2 和 p1p3 的叉积"""
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])

def is_point_on_segment(p1, p2, p):
    """判断点 p 是否在线段 p1p2 上"""
    return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])

def get_intersection_point(p1, p2, p3, p4):
    """计算两条线段 p1p2 和 p3p4 的交点"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    # 计算线段的方向向量
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    if denominator == 0:
        return None  # 平行或共线

    # 使用克莱姆法则计算交点
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    return (px, py)

def is_intersecting_with_point(p1, p2, p3, p4):
    """
    判断两条线段 p1p2 和 p3p4 是否相交，并返回交点（如果有）
    :param p1, p2: 第一条线段的端点
    :param p3, p4: 第二条线段的端点
    :return: (是否相交, 交点) 如果不相交，交点为 None
    """
    # 计算叉积，判断两条线段是否分隔两侧
    d1 = cross_product(p3, p4, p1)
    d2 = cross_product(p3, p4, p2)
    d3 = cross_product(p1, p2, p3)
    d4 = cross_product(p1, p2, p4)

    # 如果两条线段跨越对方，则它们相交
    if d1 * d2 < 0 and d3 * d4 < 0:
        intersection_point = get_intersection_point(p1, p2, p3, p4)
        return True, intersection_point

    # 如果叉积为 0，检查点是否在线段上
    if d1 == 0 and is_point_on_segment(p3, p4, p1):
        return True, p1
    if d2 == 0 and is_point_on_segment(p3, p4, p2):
        return True, p2
    if d3 == 0 and is_point_on_segment(p1, p2, p3):
        return True, p3
    if d4 == 0 and is_point_on_segment(p1, p2, p4):
        return True, p4

    return False, None

# 反查点
points = []
points_reverse = [] 
point_s = []
point_theta = []
point_turning_space = []


def dr_dtheta(theta):
    return b

def arc_length(theta):
    r = a + b * theta
    return np.sqrt(dr_dtheta(theta)**2 + r**2)


def eq_point_chain(theta2, theta1, lambda1):
    if theta2 < theta1:
        return 1e10
    if theta2 - theta1 > math.pi:
        return 1e10
    return pow(theta1, 2) + pow(theta2, 2) - 2 * theta1 * theta2 * math.cos(theta1 - theta2) - lambda1


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
    return math.atan2(r * math.cos(theta) + math.sin(theta) * b,\
                    - r * math.sin(theta) + b * math.cos(theta))


def get_point_direction_out(theta):
    r = a + b * theta
    return math.atan2(- r * math.cos(theta) - math.sin(theta) * b, r * math.sin(theta) - b * math.cos(theta))

def get_point_distance(theta, sp = 0):
    length, _ = quad(arc_length, sp, theta)
    return length 

# 生成螺线的点
theta = 0
while theta <= theta_max:
    r = a + b * theta
    x = center[0] + r * math.cos(theta)
    y = center[1] + r * math.sin(theta)
    points.append((x, y))
    
    x_reverse = center[0] - r * math.cos(-theta)
    y_reverse = center[1] + r * math.sin(-theta)
    points_reverse.append((x_reverse, y_reverse))
    
    length = get_point_distance(theta)
    
    point_s.append(length)
    point_theta.append(theta)
    
    theta += 0.1  # 角度步长，控制螺线的密度

cur_point_idx = len(points) - 2


theta = 0
while theta <= math.pi * 2:
    x = center[0] +  r_tuning_space * math.cos(theta)
    y = center[1] +  r_tuning_space * math.sin(theta)
    point_turning_space.append((x, y))
    theta += 0.01

total_length = point_s[-1]

def eq_head_point(theta, lambda1):
    return get_point_distance(theta) - lambda1
    
        
def get_distance(p1, p2):
    return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
        

def get_point_chain_next(theta1, lambda1):
    # print(theta1, lambda1)
    # theta, res = newton(eq_point_chain, theta1, args=(theta1, lambda1), maxiter=1000, full_output=True, disp=False)
    theta = root_scalar(eq_point_chain, bracket=[theta1, theta1 + math.pi], args=(theta1, lambda1), method='brentq')
    # print(theta - theta1)
    # if theta.converged:
    return theta.root, get_point_in(theta.root)
    # else:
    #     print("Not Converged", theta1)
    #     return theta1.root, get_point_in(theta1)


# 1. 计算 cos(alpha1) 和 cos(alpha2)
def cos_alpha1(b, l, theta1, theta2):
    return (b**2 * theta1**2 + l**2 - b**2 * theta2**2) / (2 * b * theta1 * l)

def cos_alpha2(b, l, theta1, theta2):
    return (b**2 * theta2**2 + l**2 - b**2 * theta1**2) / (2 * b * theta2 * l)

# 2. 计算 sin(alpha1) 和 sin(alpha2)
def sin_alpha(cos_alpha):
    return math.sqrt(1 - cos_alpha**2)

# 3. 计算 sin(beta1), cos(beta1), sin(beta2), cos(beta2)
def sin_beta(theta):
    return theta / math.sqrt(1 + theta**2)

def cos_beta(theta):
    return 1 / math.sqrt(1 + theta**2)

# 4. 计算 cos(beta1 + alpha1)
def cos_beta1_minus_alpha1(b, l, theta1, theta2):
    cos_alpha1_val = cos_alpha1(b, l, theta1, theta2)
    sin_alpha1_val = sin_alpha(cos_alpha1_val)
    cos_beta1_val = cos_beta(theta1)
    sin_beta1_val = sin_beta(theta1)

    return cos_beta1_val * cos_alpha1_val - sin_beta1_val * sin_alpha1_val

# 5. 计算 cos(alpha2 - beta2)
def cos_alpha2_plus_beta2(b, l, theta1, theta2):
    cos_alpha2_val = cos_alpha2(b, l, theta1, theta2)
    sin_alpha2_val = sin_alpha(cos_alpha2_val)
    cos_beta2_val = cos_beta(theta2)
    sin_beta2_val = sin_beta(theta2)

    return cos_alpha2_val * cos_beta2_val + sin_alpha2_val * sin_beta2_val

# 6. 最终的 v_i+1 公式
def compute_v_next(v_i, b, l, theta1, theta2):
    cos_beta1_alpha1 = cos_beta1_minus_alpha1(b, l, theta1, theta2)
    cos_alpha2_beta2 = cos_alpha2_plus_beta2(b, l, theta1, theta2)
    
    return -v_i * cos_beta1_alpha1 / cos_alpha2_beta2



paused = False

last_point_distance = []

for i in range(nodenum + 1):
    last_point_distance.append(point_s[-1])
    
f = open('output.csv', mode='w', newline='', encoding='utf-8')
fieldnames = ['time']
row_data = {}
root_data = {'time': 0}
for i in range(nodenum + 1):
    row_data['P_' + str(i)+ '_x'] = 0
    row_data['P_' + str(i)+ '_y'] = 0
    row_data['P_' + str(i)+ '_speed'] = 0
    
    fieldnames.append('P_' + str(i)+ '_x')
    fieldnames.append('P_' + str(i)+ '_y')
    fieldnames.append('P_' + str(i)+ '_speed')
    
csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
csv_writer.writeheader()

lambda1_head = (board_length_head * board_length_head) / (b  * b)
lambda1_body = (board_length * board_length) / (b  * b)


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

print(o_r)

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

def curved_distance(theta):
    if theta > intersect_theta_in:
        return get_point_distance(theta, sp = intersect_theta_in) + o_circum_1
    elif theta < -intersect_theta_out:
        return get_point_distance(-theta, sp = intersect_theta_out) - o_circum_2
    elif theta > 0:
        return theta * (o_beta / intersect_theta_in) * 2 * o_r
    else:
        return theta * (o_beta / intersect_theta_out) * o_r


def get_next_point(el_s):
    global cur_point_idx
    
    r_length = total_length - el_s
    
    while (point_s[cur_point_idx] > r_length):
        if cur_point_idx == 0:
            return points[0], 0
        cur_point_idx -= 1
        
    # tt = point_s[cur_point_idx + 1] - point_s[cur_point_idx]
    # rl = r_length - point_s[cur_point_idx]
    
    # rate = rl / tt
    
    # theta = point_theta[cur_point_idx] + rate * (point_theta[cur_point_idx + 1] - point_theta[cur_point_idx])
    
    # print(fsolve(get_point_distance, point_theta[cur_point_idx],))
    
    theta = newton(eq_head_point, point_theta[cur_point_idx], args=(r_length,))
 
    return get_point_in(theta), theta

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
    
    
    fake_screen.fill((255, 255, 255))
    distance = 0
    inner_lines = []
    checking_outer_points = []
    
    if len(points) > 1:
        pygame.draw.lines(fake_screen, (0, 0, 255), False, points, 2)
        pygame.draw.lines(fake_screen, (0, 255, 0), False, points_reverse, 2)
        
    pygame.draw.lines(fake_screen, (255, 0, 0), False, point_turning_space, 2)
    
    pygame.draw.circle(fake_screen, (0, 0, 0), intersect_in, 5)
    pygame.draw.circle(fake_screen, (0, 0, 0), intersect_out, 5)
    
    pygame.draw.lines(fake_screen, (255, 0, 0), False, [intersect_in_start, intersect_in_end], 2)
    pygame.draw.lines(fake_screen, (255, 0, 0), False, [intersect_in_cross_start, intersect_in_cross_end], 2)
    
    pygame.draw.lines(fake_screen, (0, 0, 0), False, [intersect_out_start, intersect_out_end], 2)
    pygame.draw.lines(fake_screen, (0, 0, 0), False, [intersect_out_cross_start, intersect_out_cross_end], 2)

    # pygame.draw.circle(fake_screen, (111, 111, 0), ipx_p_in, 4)
    # pygame.draw.circle(fake_screen, (111, 111, 0), ipx_p_out, 4)
    pygame.draw.circle(fake_screen, (0, 0, 0), o_point_1, 5)
    pygame.draw.circle(fake_screen, (0, 0, 0), o_point_2, 5)
    
    pygame.draw.lines(fake_screen, (255, 0, 128), False, o_point1_circle_points, 2)
    pygame.draw.lines(fake_screen, (128, 0, 255), False, o_point2_circle_points, 2)
    
    theta = 20
    while theta >= -20:
        pygame.draw.circle(fake_screen, ( abs(255 * (theta / 100)), abs(255 * (theta / 100)), 0), curved(theta), 2 )
        theta -= 0.01
        
    theta = - (time) * 1 + 1
    
    pygame.draw.circle(fake_screen, ( 255, 0, 0), curved(theta), 10)
    
    GAME_FONT.render_to(fake_screen, (500, 30), f"THETA:{theta:.3f} DIS: {curved_distance(theta)}", (0, 0, 0))

    current_s = time * speed
    
    head_point, theta1 = get_next_point(current_s)
    
    pygame.draw.circle(fake_screen, (255, 0, 0), head_point, 5)
    
    sec_point_theta = theta1
    sec_point = head_point
    speed_ = speed
    # speed__ = speed     
    
    for i in range(nodenum):
        
        if sec_point_theta - theta1 > 3 * math.pi:
            break
        
        if i == 0:
            _sec_point_theta, _sec_point = get_point_chain_next(sec_point_theta, lambda1_head)
        else:
            _sec_point_theta, _sec_point = get_point_chain_next(sec_point_theta, lambda1_body)
            
        pygame.draw.circle(fake_screen, (0, 255 * (i/nodenum), 255 * (i/nodenum)), _sec_point, 3)
        
        _distance = get_distance(sec_point, _sec_point)
        distance += _distance
        
        
        pts = get_board_points(_sec_point, sec_point)
        pygame.draw.lines(fake_screen, (128, 128, 128), True, pts, 1)
        # for pt in pts[0:1]:
        # pygame.draw.circle(fake_screen, (116, 152, 93), pts[0], 4)
        # pygame.draw.circle(fake_screen, (116, 152, 93), pts[3], 4)
        pygame.draw.line(fake_screen, (0, 0, 0), pts[0], pts[3], 1)
        
        if i > 3:
            inner_lines.append((pts[0], pts[3]))
        
        if i == 0 or i == 1:
            checking_outer_points.append((pts[1], pts[2]))
            checking_outer_points.append((pts[1], pts[0]))
            checking_outer_points.append((pts[3], pts[2]))
            
        this_dis = get_point_distance(sec_point_theta)
        
        # speed__ = (this_dis - last_point_distance[i]) / delta_t
        
        p_x = sec_point[0] - center[0]
        p_y = - sec_point[1] + center[1]
  
        row_data['P_' + str(i)+ '_x'] = p_x
        row_data['P_' + str(i)+ '_y'] = p_y
        row_data['P_' + str(i)+ '_speed'] = speed_
        
        if i < 15:
            GAME_FONT.render_to(fake_screen, (10, 130 + 25 * (i)), f"P_{i:3}: {_distance:.5f} {sec_point_theta:.8f} {p_x:12.5f},{p_y:12.5f} {speed_:10.5f}" , (0, 0, 0))

        speed_ = compute_v_next(speed_, b, board_length_head if i == 0 else board_length, sec_point_theta , _sec_point_theta)
        
        sec_point = _sec_point
        sec_point_theta = _sec_point_theta
        # last_point_distance[i] = this_dis
    
    row_data['time'] = time
    csv_writer.writerow(row_data)
    
    GAME_FONT.render_to(fake_screen, (10, 10), "DIS: " + str(distance), (0, 0, 0))
    GAME_FONT.render_to(fake_screen, (10, 30), "FPS: " + str(clock.get_fps()), (0, 0, 0))
    GAME_FONT.render_to(fake_screen, (10, 50), "TIME: " + str(time), (0, 0, 0))
    
    center_Dis = get_distance(head_point, center)
    
    GAME_FONT.render_to(fake_screen, (10, 80), f"CENTER DIS: {center_Dis}", (255, 0, 0) if center_Dis > r_tuning_space else (0, 255, 0))
        
    # if center_Dis <= r_tuning_space:
    #     # paused = True
    #     print("Center Intersect ", time)

    intersection_points = []
    HAS_INTERSECT = False
    
    for pt in checking_outer_points:
        pygame.draw.lines(fake_screen, (0, 0, 255), False, pt, 2)

        P = None
        for i in range(len(inner_lines)):
            w, P = is_intersecting_with_point(inner_lines[i][0], inner_lines[i][1], pt[0], pt[1])
            if w:
                HAS_INTERSECT = True
                intersection_points.append(P)
                break
            
    if HAS_INTERSECT:
        paused = True
        print("Intersect", pt, inner_lines[i], time)
        GAME_FONT.render_to(fake_screen, (10, 110), f"Intersect at: {intersection_points}", (255, 0, 0))
        for pt in intersection_points:
            pygame.draw.circle(fake_screen, (255, 0, 0), pt, 5)
    else:
        GAME_FONT.render_to(fake_screen, (10, 110), f"Not Intersect", (0, 255, 0))

    screen.blit(pygame.transform.smoothscale(fake_screen, screen.get_size()), (0, 0))
    pygame.display.flip()
    clock.tick()

    time += delta_t

pygame.quit()