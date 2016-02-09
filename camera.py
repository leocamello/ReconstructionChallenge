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

from pyramid import Pyramid
from plane import Plane


class Rectangle:
    def __init__(self):
        self.bottomLeft = np.array([-0.5, -0.5, 0.0], np.float32)
        self.topLeft = np.array([-0.5, 0.5, 0.0], np.float32)
        self.topRight = np.array([0.5, 0.5, 0.0], np.float32)
        self.bottomRight = np.array([0.5, -0.5, 0.0], np.float32)


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
        # coordinate system
        self.coordSystem = { "x": np.array([1.0, 0.0, 0.0], np.float32),
                             "y": np.array([0.0, 1.0, 0.0], np.float32),
                             "z": np.array([0.0, 0.0, 1.0], np.float32) }


    def loadImage(self, imagePath):
        img = image.read(imagePath)
        self.image['width'] = img[0]
        self.image['height'] = img[1]
        self.image['data'] = img[2]


    def adjustRotation(self, yaw, pitch, roll):
        rotation = mat.rotation(yaw, pitch, roll)
        self.coordSystem['x'] = mat.vec3(np.dot(rotation, mat.vec4(self.coordSystem['x'])))
        self.coordSystem['y'] = mat.vec3(np.dot(rotation, mat.vec4(self.coordSystem['y'])))
        self.coordSystem['z'] = mat.vec3(np.dot(rotation, mat.vec4(self.coordSystem['z'])))


    def setPosition(self, x, y, z):
        self.position = np.array([x, y, z], np.float32)


    def ray(self, x, y):
        u = self.canvas['width'] * ((x / self.image['width']) - 0.5)
        v = self.canvas['height'] * ((y / self.image['height']) - 0.5)
        w = -self.zPlane['near']
        a = np.array(self.coordSystem['x'] * u)
        b = np.array(self.coordSystem['y'] * v)
        c = np.array(self.coordSystem['z'] * w)
        d = mat.normalize((a + b) + c)
        return d


    def intersection(self, ray):
        v0 = np.array([0.0, 0.0, 0.0], np.float32)
        normal = np.array([0.0, 0.0, 0.1], np.float32)
        num = np.dot(normal, v0 - self.position)
        den = np.dot(normal, ray)
        t = num / den
        return self.position + t * ray


    def initialize(self):
        rect = Rectangle()
        rect.bottomLeft = self.intersection(self.ray(0, 0))
        rect.topLeft = self.intersection(self.ray(0, self.image['height']))
        rect.topRight = self.intersection(self.ray(self.image['width'], self.image['height']))
        rect.bottomRight = self.intersection(self.ray(self.image['width'], 0.0))
        self.pyramid = Pyramid(self.position, rect)
        self.plane = Plane(rect, self.image)


    def display(self, width, height, z, current=False, frustrum=False):
        self.plane.draw(width, height, z)
        if frustrum:
            self.pyramid.draw(width, height, z, current)
