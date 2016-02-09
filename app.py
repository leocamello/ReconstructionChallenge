#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 16:15:00 2016

@author: Leonardo Nascimento
"""

import csv, math

import numpy as np

from camera import Camera

# data in meters
film = { "35mm": { "width": 0.036, "height": 0.024 } }
focalLength = 0.020


def calculateDistance(p0, p1):
    r = 6371000
    fi1 = math.radians(p0[1])
    fi2 = math.radians(p1[1])
    deltafi = math.radians(p1[1] - p0[1])
    deltalambda = math.radians(p1[0] - p0[0])
    a = math.sin(deltafi / 2) * math.sin(deltafi / 2) + math.cos(fi1) * math.cos(fi2) * math.sin(deltalambda / 2) * math.sin(deltalambda / 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r * c

class Application:
    def __init__(self, csvFile, imagesPath):
        infos = []
        with open(csvFile) as cameraInfo:
            for info in csv.DictReader(cameraInfo):
                inf = {}
                inf['image'] = (imagesPath + info['# Filename'])
                inf['position'] = (np.array([float(info['X']), float(info['Y']), float(info['Z'])]))
                inf['rotation'] = ((-float(info['Yaw']), -float(info['Pitch']), -float(info['Roll'])))
                infos.append(inf)

        center = np.array(infos[0]['position'])

        for info in infos[1:]:
            center += info['position']

        center = center / len(infos)
 
        self.cameras = []
        for info in infos:
            camera = Camera(film['35mm'], focalLength, info['image'])
            camera.adjustRotation(info['rotation'][0],info['rotation'][1],info['rotation'][2])
            p = info['position']
            x = calculateDistance(center, (p[0], center[1], p[2]))
            y = calculateDistance(center, (center[0], p[1], p[2]))
            if center[0] > p[0]:
                x = -x
            if center[1] > p[1]:
                y = -y
            camera.setPosition(x, y, p[2])
            camera.initialize()
            self.cameras.append(camera)


    def display(self, width, height):
        for camera in self.cameras:
            camera.display(np.zeros(3), width, height)