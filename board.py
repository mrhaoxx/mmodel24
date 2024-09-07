import math

board_outer_width = 027.5
board_width = 30.

board_length_head = 341 - 55
board_length = 220 - 55

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
