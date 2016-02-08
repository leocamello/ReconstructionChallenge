#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 16:15:00 2016

@author: Leonardo Nascimento
"""

import csv

# data in meters
film = { "35mm": { "width": 0.036, "height": 0.024 } }
focalLength = 0.020


class Application:
    def __init__(self, csvFile, imagesPath):
        with open(csvFile) as cameraInfo:
            for info in csv.DictReader(cameraInfo):
                print(info)