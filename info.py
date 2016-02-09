#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 09 13:30:00 2016

@author: Leonardo Nascimento
"""

import math
import numpy as np


earthRadius = 6371000
def distance(lat1, lon1, lat2, lon2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dPhi = math.radians(lat2 - lat1)
    dTetha = math.radians(lon2 - lon1)
    a = math.sin(dPhi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dTetha / 2) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return earthRadius * c


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