import numpy as np
from math import *



def translate(x, y, z, points):
    translation_matrix = np.matrix([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])
    translated_points = []
    for point in points:
        translated_points.append(np.dot(translation_matrix, point))
        print(translated_points[-1])
    return translated_points

def rotate(angle, axis, points):
    if axis == 'x':
        rotation_matrix = np.matrix([
            [1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])
    if axis == 'y':
        rotation_matrix = np.matrix([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])
    if axis == 'z':
        rotation_matrix = np.matrix([
            [cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    rotated_points = []
    for point in points:
        rotated_points.append(np.dot(rotation_matrix, point))
    return rotated_points
