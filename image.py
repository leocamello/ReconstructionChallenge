#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 15:20:00 2016

@author: Leonardo Nascimento
"""

from PIL import Image
from ctypes import string_at


def read(path):
    image = Image.open(imagePath)
    width = image.size[0]
    height = image.size[1]
    try:
        data = image.tostring("raw", "RGBX", 0, -1)
    except:
        data = image.tostring("raw", "RGBA", 0, -1)
    return (width, height, data)


def write(width, height, data, size):
    image = Image.fromstring("RGBA", (width, height), string_at(data, size))
    image.save("out.png", "PNG")