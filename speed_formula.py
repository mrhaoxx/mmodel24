import math
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