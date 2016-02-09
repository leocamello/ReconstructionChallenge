#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 16:15:00 2016

@author: Leonardo Nascimento
"""

import csv

from camera import Camera

# data in meters
film = { "35mm": { "width": 0.036, "height": 0.024 } }
focalLength = 0.020


class Application:
    def __init__(self, csvFile, imagesPath):
        self.cameras = []

        with open(csvFile) as cameraInfo:
            for info in csv.DictReader(cameraInfo):
                camera = Camera(film['35mm'], focalLength, imagesPath + info['# Filename'])
                camera.adjustRotation(float(info['Yaw']), float(info['Pitch']), float(info['Roll']))
                camera.setPosition(float(info['X']), float(info['Y']), float(info['Z']))
                #camera.initialize()

                self.cameras.append(camera)


    def display(self):
        pass
    #    for camera in cameras:
    #        camera.display()