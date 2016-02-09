#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 16:15:00 2016

@author: Leonardo Nascimento
"""

import csv, math

import numpy as np

from info import Info
from camera import Camera

# data in meters
film = { "35mm": { "width": 0.036, "height": 0.024 } }
focalLength = 0.020

class Application:
    def __init__(self, csvFile, imagesPath):

        self.cameraIndex = 0
        self.displayFrustrum = False
        
        # Reading camera information from csv file
        infos = []
        with open(csvFile) as csvEntries:
            for entry in csv.DictReader(csvEntries):
                infos.append(Info(entry['# Filename'], entry['X'], entry['Y'], entry['Z'], entry['Yaw'], entry['Pitch'], entry['Roll']))
                

        # Calculating central lat/lon
        center = np.zeros(2)
        for info in infos:
            center += np.array([info.latitude, info.longitude])
        center = center / len(infos)


        # Creating our cameras
        # Their position is relative to the center
        self.cameras = []
        for info in infos:
            imagePath = imagesPath + info.filename
            camera = Camera(film['35mm'], focalLength, imagePath)
            camera.adjustRotation(info.yaw, info.pitch, info.roll)
            camera.setPosition(*info.relativeXYZ(*center))
            camera.initialize()

            self.cameras.append(camera)

        # Sorting cameras related to center
        def getKey(item):
            return np.linalg.norm(item.position)
        self.cameras = sorted(self.cameras, key=getKey)
        self.cameras.reverse()


    def display(self, width, height):
        j = self.cameraIndex % len(self.cameras)
        for i in range(len(self.cameras)):
            if i != j:
                self.cameras[i].display(width, height, 500, False, self.displayFrustrum)
        self.cameras[j].display(width, height, 500, True, self.displayFrustrum)


    def frustrum(self):
        self.displayFrustrum = not self.displayFrustrum
            

    def next(self):
        self.cameraIndex += 1


    def previous(self):
        self.cameraIndex -= 1