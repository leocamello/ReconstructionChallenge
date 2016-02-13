#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 09 13:30:00 2016

@author: Leonardo Nascimento
"""

import math
import numpy as np
import pyproj


def distance(lat1, lon1, lat2, lon2):
    geod = pyproj.Geod(ellps="WGS84")
    angle1, angle2, distance = geod.inv(lon1, lat1, lon2, lat2)
    return distance


class Info():
    def __init__(self, filename, x, y, z, yaw, pitch, roll):
        self.filename = filename
        self.longitude = float(x)
        self.latitude = float(y)
        self.z = float(z)
        self.yaw = -1.0 * float(yaw)
        self.pitch = -1.0 * float(pitch)
        self.roll = -1.0 * float(roll)


    def relativeXYZ(self, latitude, longitude):
        XYZ = np.zeros(3)
        XYZ[2] = self.z
        dY = distance(latitude, longitude, self.latitude, longitude)
        XYZ[1] = dY if self.latitude > latitude else -dY
        dX =  distance(latitude, longitude, latitude, self.longitude)
        XYZ[0] = dX if self.longitude > longitude else -dX
        return XYZ

    def distance(self, latitude, longitude):
        return distance(latitude, longitude, self.latitude, self.longitude)