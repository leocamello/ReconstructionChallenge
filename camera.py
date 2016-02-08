#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 17:29:00 2016

@author: Leonardo Nascimento
"""

import image

import numpy as np
import matrix as mat

from math import tan, atan
from math import radians, degrees


class Camera:
    def __init__(self, filmSize, focalLength, imagePath):
        # intrinsic parameters
        self.fieldOfView = { "x": 0.0, "y": 0.0 }
        self.fieldOfView['x'] = 2.0 * atan(filmSize['width'] / (2.0 * focalLength))
        self.fieldOfView['y'] = 2.0 * atan(filmSize['height'] / (2.0 * focalLength))
        self.zPlane = { "near": 0.1, "far": 1000.0 }
        self.image = { "width": 0.0, "height": 0.0, "data": None }
        self.loadImage(imagePath)
        self.canvas = { "width": 0.0, "height": 0.0 }
        self.canvas['width'] = 2.0 * tan(self.fieldOfView['x'] / 2.0) * self.zPlane['near']
        self.canvas['height'] = 2.0 * tan(self.fieldOfView['y'] / 2.0) * self.zPlane['near']
        # extrinsic parameters
        self.position = np.array([0.0, 0.0, 0.0], np.float32)
        self.center = np.array([0.0, 0.0, -1.0], np.float32)
        self.up = np.array([0.0, 1.0, 0.0], np.float32)
        # coordinate system
        self.coordSystem = { "x": np.array([0.0, 0.0, 0.0], np.float32),
                             "y": np.array([0.0, 0.0, 0.0], np.float32),
                             "z": np.array([0.0, 0.0, 0.0], np.float32) }
        self.updateCoordSystem()


    def adjustRotation(self, yaw, pitch, roll):
        rotation = mat.rotation(yaw, pitch, roll)
        self.position = mat.vec3(np.dot(rotation, mat.vec4(self.position)))
        self.center = mat.vec3(np.dot(rotation, mat.vec4(self.center)))
        self.up = mat.vec3(np.dot(rotation, mat.vec4(self.up)))
        self.updateCoordSystem()


    def setPosition(self, x, y, z):
        self.position = np.array([x, y, z], np.float32)
        self.updateCoordSystem()


    def updateCoordSystem(self):
        self.coordSystem['z'] = mat.normalize(self.position - self.center)
        self.coordSystem['x'] = mat.normalize(np.cross(self.up, self.coordSystem['z']))
        self.coordSystem['y'] = mat.normalize(np.cross(self.coordSystem['z'], self.coordSystem['x']))


    def loadImage(self, imagePath):
        img = image.read(imagePath)
        self.image['width'] = img[0]
        self.image['height'] = img[1]
        self.image['data'] = img[2]


    def ray(self, x, y):
        u = self.canvas['width'] * ((x / self.image['width']) - 0.5)
        v = self.canvas['height'] * ((y / self.image['height']) - 0.5)
        w = -self.zPlane['near']
        a = np.array(self.coordSystem['x'] * u)
        b = np.array(self.coordSystem['y'] * v)
        c = np.array(self.coordSystem['z'] * w)
        d = mat.normalize((a + b) + c)
        return d