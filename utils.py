import math 
import numpy as np

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


def get_distance(p1, p2):
    return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
        
def Cosine(a, b, c):
    return math.acos((a * a + b * b - c * c) / (2 * a * b))


def point_to_segment_distance(point, seg_start, seg_end):
    # 将点和线段的起始点、终点转换为 numpy 向量
    point = np.array(point)
    seg_start = np.array(seg_start)
    seg_end = np.array(seg_end)
    
    # 线段的向量
    seg_vector = seg_end - seg_start
    point_vector = point - seg_start
    
    # 线段长度的平方
    seg_len_sq = np.dot(seg_vector, seg_vector)
    
    if seg_len_sq == 0:
        # 线段的起点和终点重合，则直接返回点到起点的距离
        return np.linalg.norm(point - seg_start)
    
    # 计算投影的比例 t
    t = np.dot(point_vector, seg_vector) / seg_len_sq
    
    # 限制 t 在 [0, 1] 范围内，表示点在线段的投影
    t = max(0, min(1, t))
    
    # 计算最近的点
    nearest_point = seg_start + t * seg_vector
    
    # 返回点到最近点的距离
    return np.linalg.norm(point - nearest_point)
