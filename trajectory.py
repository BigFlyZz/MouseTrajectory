import random

import numpy as np
from scipy.special import comb


def generate_random_points_on_line(point1, point2, n):
    distance = np.linalg.norm(point2 - point1)
    random_weights = np.random.random(n - 2)
    random_points = (1 - random_weights)[:, np.newaxis] * point1 + random_weights[:, np.newaxis] * point2
    random_offsets = np.random.uniform(-distance / 2, distance / 2, n - 2)
    direction_vector = point2 - point1
    unit_direction_vector = direction_vector / np.linalg.norm(direction_vector)
    perpendicular_vector = np.array([-unit_direction_vector[1], unit_direction_vector[0]])
    random_points_with_offsets = random_points + random_offsets[:, np.newaxis] * perpendicular_vector
    random_points_with_endpoints = np.vstack([point1, random_points_with_offsets, point2])
    return random_points_with_endpoints


def bezier_curve(control_points, num_points=50):
    num_points = num_points + 1
    n = len(control_points) - 1
    acceleration_factor = 1.8 + random.random()
    deceleration_factor = 1.8 + random.random()
    t = np.linspace(0, 1, num_points)
    t = np.power(t, acceleration_factor) / (
            np.power(t, acceleration_factor) + np.power(1 - t, deceleration_factor))

    curve = np.zeros((num_points, 2))
    for i in range(num_points):
        for j in range(n + 1):
            curve[i] += comb(n, j) * (1 - t[i]) ** (n - j) * t[i] ** j * control_points[j]

    return curve


def generate_smooth_trajectory(point1, point2, num_points):
    # 定义两个点的坐标
    point1 = np.array(point1)
    point2 = np.array(point2)

    point3 = point2 + np.random.uniform(-50, 50)
    print(point3)
    # 定义要生成的点的数量
    num_points = 1000

    # 调用函数生成随机点
    random_points = generate_random_points_on_line(point1, point3, 6)
    random_points_1 = generate_random_points_on_line(point3, point2, 3)

    curve = bezier_curve(random_points, num_points)
    curve_1 = bezier_curve(random_points_1, 200)
    return np.concatenate((curve, curve_1), axis=0)


'''
for (x, y) in generate_smooth_trajectory((1, 1), (456, 895), 1000):
    print(x, y)
    try:
        pyautogui.moveTo(int(x), int(y), tween=lambda n: n, _pause=False)
    except pyautogui.FailSafeException:
        pass
    time.sleep(1 / 1000)
'''
