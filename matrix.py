#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 17:00:00 2016

@author: Leonardo Nascimento
"""

import numpy as np
from math import sin, cos, tan, radians

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


def vec3(v):
    return np.array([v[0], v[1], v[2]], np.float32)


def vec4(v):
    return np.array([v[0], v[1], v[2], 1.0], np.float32)


def translation(v):
    return np.array([[1.0, 0.0, 0.0, v[0]],
                     [0.0, 1.0, 0.0, v[1]],
                     [0.0, 0.0, 1.0, v[2]],
                     [0.0, 0.0, 0.0, 1.0]])


def rotation(angle, axis):
    s = sin(radians(angle))
    c = cos(radians(angle))
    return np.array([[c + axis[0] * axis[0] * (1 - c), axis[0] * axis[1] * (1 - c) - axis[2] * s, axis[0] * axis[2] * (1 - c) + axis[1] * s, 0.0],
                     [axis[1] * axis[0] * (1 - c) + axis[2] * s, c + axis[1] * axis[1] * (1 - c), axis[1] * axis[2] * (1 - c) - axis[0] * s, 0.0],
                     [axis[2] * axis[0] * (1 - c) - axis[1] * s, axis[2] * axis[1] * (1 - c) + axis[0] * s, c + axis[2] * axis[2] * (1 - c), 0.0],
                     [0.0, 0.0, 0.0, 1.0]])


def rotation(yaw, pitch, roll):
    yaw, pitch, roll = map(radians, [yaw, pitch, roll])
    return np.array([[cos(yaw) * cos(pitch), cos(yaw) * sin(pitch) * sin(roll) - sin(yaw) * cos(roll), cos(yaw) * sin(pitch) * cos(roll) + sin(yaw) * sin(roll), 0.0],
                     [sin(yaw) * cos(pitch), sin(yaw) * sin(pitch) * sin(roll) + cos(yaw) * cos(roll), sin(yaw) * sin(pitch) * cos(roll) - cos(yaw) * sin(roll), 0.0],
                     [          -sin(pitch),                                   cos(pitch) * sin(roll),                                   cos(pitch) * cos(roll), 0.0],
                     [0.0, 0.0, 0.0, 1.0]])


def scale(f):
    return np.array([[f[0], 0.0, 0.0, 0.0],
                     [0.0, f[1], 0.0, 0.0],
                     [0.0, 0.0, f[2], 0.0],
                     [0.0, 0.0, 0.0, 1.0]])


def perspective(fov, aspect, near, far):
    f = 1.0 / tan(radians(fov / 2.0))
    return np.array([[f / aspect, 0.0, 0.0, 0.0],
                     [0.0, f, 0.0, 0.0],
                     [0.0, 0.0, (far + near) / (near - far), (2.0 * far * near) / (near - far)],
                     [0.0, 0.0, -1.0, 0.0]])