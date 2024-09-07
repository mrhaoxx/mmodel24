import math

from scipy.optimize import newton, root_scalar
from utils import get_distance, get_intersection_point


class loong:
    def get_point_in(self, theta):
        r = self.a + self.b * theta
        x = + r * math.cos(theta)
        y = + r * math.sin(theta)
        return x, y

    def get_point_out(self, theta):
        r = self.a + self.b * theta
        x = - r * math.cos(-theta)
        y = + r * math.sin(-theta)
        return x, y


    def get_point_direction_in(self, theta):
        r = self.a + self.b * theta
        return math.atan2(r * math.cos(theta) + math.sin(theta) * self.b,- r * math.sin(theta) + self.b * math.cos(theta))

    def get_point_direction_out(self, theta):
        r = self.a + self.b * theta
        return math.atan2(- r * math.cos(theta) - math.sin(theta) * self.b, r * math.sin(theta) - self.b * math.cos(theta))


    def eq_intersect_in_track(self, theta, target_dis, curve):
        return get_distance(curve(theta), (0,0)) - target_dis

    def get_point_posR(self, theta):
        x = self.o_point_1[0] + 2 * self.o_r * math.cos(theta)
        y = self.o_point_1[1] + 2 * self.o_r * math.sin(theta)
        return x, y
        
    def get_point_negR(self, theta):
        x = self.o_point_2[0] + self.o_r * math.cos(theta)
        y = self.o_point_2[1] + self.o_r * math.sin(theta)
        return x, y


    def curved(self, theta):
        if theta > self.intersect_theta_in:
            return self.get_point_in(theta)
        elif theta < -self.intersect_theta_out:
            return self.get_point_out(-theta)
        elif theta > 0:
            return self.get_point_posR(theta * (self.o_beta / self.intersect_theta_in) +  self.intersect_theta_in +  math.pi + (math.pi - self.o_beta) / 2)
        else:
            return self.get_point_negR(-theta * (self.o_beta / self.intersect_theta_out) + self.intersect_theta_out  + (math.pi - self.o_beta) / 2)


    def get_point_distance_in(self, theta):
        return self.c_bsquared2 * (theta * math.sqrt(1 + theta * theta) + math.log(theta + math.sqrt(1 + theta * theta))) - self.c_sp_in
    

    def get_point_distance_out(self, theta):
        return self.c_bsquared2 * (theta * math.sqrt(1 + theta * theta) + math.log(theta + math.sqrt(1 + theta * theta))) - self.c_sp_out
        
    

    def curved_distance(self, theta):
        if theta > self.intersect_theta_in:
            return self.get_point_distance_in(theta) + self.o_circum_1
        elif theta < -self.intersect_theta_out:
            return - self.get_point_distance_out(-theta) - self.o_circum_2
        elif theta > 0:
            return theta * (self.o_beta / self.intersect_theta_in) * 2 * self.o_r
        else:
            return theta * (self.o_beta / self.intersect_theta_out) * self.o_r





    def eq_point_chain_sim(self, theta2, point1, distance):
        return (get_distance(self.curved(theta2), point1) - distance)
        

    def get_point_chain_next_sim(self, theta1, point1, distance):
        itec = math.pi / 4
        
        while self.eq_point_chain_sim(theta1 + itec, point1, distance) < 0:
            itec += math.pi / 4
            
        theta = root_scalar(self.eq_point_chain_sim, bracket=[theta1, theta1 + itec], args=(point1, distance), method='brentq')
        return theta.root, self.curved(theta.root)

    def eq_head_point(self, theta, lambda1):
        return self.curved_distance(theta) - lambda1


    def get_head_point(self, el_s):
        
        r_length = self.total_length - el_s
        
        while (self.points_s[self.cur_point_idx] >= r_length):
            if self.cur_point_idx == 0:
                return self.points[0], 0
            self.cur_point_idx -= 1

        # print(self.cur_point_idx)
        # print(self.points_s[self.cur_point_idx-1], self.points_s[self.cur_point_idx+1], r_length)
        # print(self.eq_head_point(self.points_theta[self.cur_point_idx-1], r_length), self.eq_head_point(self.points_theta[self.cur_point_idx+1], r_length))
        theta = root_scalar(self.eq_head_point, bracket=[self.points_theta[self.cur_point_idx], self.points_theta[self.cur_point_idx+1]], args=(r_length,))
        return self.curved(theta.root), theta.root

    def get_looong(self, distance_from_starting_point):

        head_point, theta1 = self.get_head_point(distance_from_starting_point)
            
            
        points_result = []
        
        sec_point_theta = theta1
        sec_point = head_point
        
        for i in range(self.nodenum + 1):
            points_result.append(sec_point)
            
            if i == self.nodenum:
                pass
            else:
                sec_point_theta, sec_point = self.get_point_chain_next_sim(sec_point_theta, sec_point, self.board_length_head if i == 0 else self.board_length)
        
        return points_result
    
    def __init__(self, pitch = 170, theta_max = 32 * math.pi, nodenum = 223, r_turning_space = 450) -> None:
        
        self.a = 0
        self.b = pitch / (2 * math.pi)
        self.theta_max = theta_max
        self.r_tuning_space = r_turning_space
        self.nodenum = nodenum

        self.board_outer_width = 27.5
        self.board_width = 30.
        self.board_length_head = 341 - 55
        self.board_length = 220 - 55



        self.board_alpha = math.atan2(self.board_outer_width, (self.board_width / 2))
        self.board_slash = math.sqrt(pow(self.board_outer_width, 2) + pow(self.board_width / 2, 2))
        self.board_beta = 2*math.atan2(self.board_width / 2, self.board_outer_width)


        # 螺旋线与转弯空间的交点的 theta, 进入方向
        self.intersect_theta_in = newton(self.eq_intersect_in_track, 0, args=(self.r_tuning_space,self.get_point_in))

        # 进入方向： 螺旋线的切线方向
        self.intersect_theta_in_direction_theta = self.get_point_direction_in(self.intersect_theta_in)

        # 进入方向： 螺旋线的法线方向
        self.intersect_theta_in_direction_theta_perpendicular = self.intersect_theta_in_direction_theta + math.pi / 2
        self.intersect_in = self.get_point_in(self.intersect_theta_in)

        self.intersect_in_start = (self.intersect_in[0] - 100 * math.cos(self.intersect_theta_in_direction_theta), self.intersect_in[1] - 100 * math.sin(self.intersect_theta_in_direction_theta))
        self.intersect_in_end = (self.intersect_in[0] + 100 * math.cos(self.intersect_theta_in_direction_theta), self.intersect_in[1] + 100 * math.sin(self.intersect_theta_in_direction_theta))
        self.intersect_in_cross_start = (self.intersect_in[0] - 1000 * math.cos(self.intersect_theta_in_direction_theta_perpendicular), self.intersect_in[1] - 1000 * math.sin(self.intersect_theta_in_direction_theta_perpendicular))
        self.intersect_in_cross_end = (self.intersect_in[0] + 1000 * math.cos(self.intersect_theta_in_direction_theta_perpendicular), self.intersect_in[1] + 1000 * math.sin(self.intersect_theta_in_direction_theta_perpendicular))

        self.intersect_theta_out = newton(self.eq_intersect_in_track, 0, args=(self.r_tuning_space,self.get_point_out))

        self.intersect_theta_out_direction_theta = self.get_point_direction_out(self.intersect_theta_out)
        self.intersect_theta_out_direction_theta_perpendicular = self.intersect_theta_out_direction_theta + math.pi / 2

        self.intersect_out = self.get_point_out(self.intersect_theta_out)
        self.intersect_out_start = (self.intersect_out[0] - 100 * math.cos(self.intersect_theta_out_direction_theta), self.intersect_out[1] - 100 * math.sin(self.intersect_theta_out_direction_theta))
        self.intersect_out_end = (self.intersect_out[0] + 100 * math.cos(self.intersect_theta_out_direction_theta), self.intersect_out[1] + 100 * math.sin(self.intersect_theta_out_direction_theta))
        self.intersect_out_cross_start = (self.intersect_out[0] - 1000 * math.cos(self.intersect_theta_out_direction_theta_perpendicular), self.intersect_out[1] - 1000 * math.sin(self.intersect_theta_out_direction_theta_perpendicular))
        self.intersect_out_cross_end = (self.intersect_out[0] + 1000 * math.cos(self.intersect_theta_out_direction_theta_perpendicular), self.intersect_out[1] + 1000 * math.sin(self.intersect_theta_out_direction_theta_perpendicular))

        self.intersect_in_point_intersect = get_intersection_point(self.intersect_in_start, self.intersect_in_end, self.intersect_out_cross_end, self.intersect_out_cross_start)
        self.intersect_out_point_intersect = get_intersection_point(self.intersect_out_start, self.intersect_out_end, self.intersect_in_cross_end, self.intersect_in_cross_start)

        self.o_w = get_distance(self.intersect_out_point_intersect, self.intersect_out)
        self.o_l = get_distance(self.intersect_in_point_intersect, self.intersect_out)

        # print(o_w, o_l)

        self.phi = math.atan(1/self.intersect_theta_in)

        self.o_r = self.r_tuning_space / (3 * math.cos(self.phi))

        rate_1 = 2 * self.o_r / self.o_l
        rate_2 = self.o_r / self.o_l

        self.o_point_1 = (self.intersect_in[0] * (1 - rate_1) + self.intersect_out_point_intersect[0] * rate_1, self.intersect_in[1] * (1 - rate_1) + self.intersect_out_point_intersect[1] * rate_1)
        self.o_point_2 = (self.intersect_out[0] * (1 - rate_2) + self.intersect_in_point_intersect[0] * rate_2, self.intersect_out[1] * (1 - rate_2) + self.intersect_in_point_intersect[1] * rate_2)

        self.o_beta = (math.pi - math.asin(self.o_w / (3 * self.o_r)))

        self.o_circum_1 = self.o_beta * 2 * self.o_r
        self.o_circum_2 = self.o_beta * self.o_r


        self.c_bsquared2 = self.b / 2

        self.c_sp_in = self.c_bsquared2 * (self.intersect_theta_in * math.sqrt(1 + self.intersect_theta_in * self.intersect_theta_in) + math.log(self.intersect_theta_in + math.sqrt(1 + self.intersect_theta_in * self.intersect_theta_in)))

        self.c_sp_out = self.c_bsquared2 * (self.intersect_theta_out * math.sqrt(1 + self.intersect_theta_out * self.intersect_theta_out) + math.log(self.intersect_theta_out + math.sqrt(1 + self.intersect_theta_out * self.intersect_theta_out)))


        self.points = []
        self.points_s = []
        self.points_theta = []

        # 生成螺线的点
        theta =  - self.theta_max
        while theta <= self.theta_max:
            self.points.append(self.curved(theta))
            self.points_s.append(self.curved_distance(theta))
            self.points_theta.append(theta)
            
            theta += 0.01 

        self.cur_point_idx = len(self.points) - 2

        self.total_length = self.points_s[-1]

    
    def get_board_points(self, pt1, pt2):
        theta = math.atan2((pt1[1] - pt2[1]),(pt2[0] - pt1[0]))
        
        alpha = math.pi / 2 - theta - self.board_alpha
        
        d1 = (self.board_slash * math.cos(alpha))
        d2 = (self.board_slash * math.sin(alpha))
        
        sigma = (math.pi / 2 ) - self.board_beta + alpha
        
        d3 = self.board_slash * math.cos(sigma)
        d4 = self.board_slash * math.sin(sigma)
        
        x1 = pt1[0] - d1
        y1 = pt1[1] - d2
        
        x2 = pt1[0] - d4
        y2 = pt1[1] + d3
        
        x3 = pt2[0] + d1
        y3 = pt2[1] + d2
        
        x4 = pt2[0] + d4
        y4 = pt2[1] - d3
        
        return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
            
            
def get_ptr_speeds(points_before, points_after, interval):
    speeds = []
    for i in range(len(points_before)):
        distance = get_distance(points_before[i], points_after[i])
        speeds.append(distance / interval)
    return speeds

def get_speed(l: loong, time, speed, interval = 1e-4):
    if time - interval < 0:
        points_before = l.get_looong(time * speed)
        points_after = l.get_looong((time + interval) * speed)
        return get_ptr_speeds(points_before, points_after, interval)
    
    points_before = l.get_looong((time - interval) * speed) 
    points_after = l.get_looong((time + interval) * speed)
    return get_ptr_speeds(points_before, points_after, 2 * interval)
