#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 14:00:00 2016

@author: Leonardo Nascimento
"""

import sys
import image

from OpenGL.GL import *
from OpenGL.GLUT import *

from app import Application


WINDOW_SIZE = 1024, 768


def display():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    app.display(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)


def keyboard(key, x, y):
    if key == "s":
        app.screenShot()

    glutPostRedisplay()


def motion(x, y):
    pass


def mouse(button, state, x, y):
    pass


def screenShot():
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)

    # rgba data size
    size = width * height * 4
    
    pixelBuffer = glGenBuffers(1)
    glBindBuffer(GL_PIXEL_PACK_BUFFER, pixelBuffer)
    glBufferData(GL_PIXEL_PACK_BUFFER, size, None, GL_STREAM_READ)
    glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, c_void_p(0))
    data = glMapBuffer(GL_PIXEL_PACK_BUFFER, GL_READ_ONLY)
    
    image.write(width, height, data, size)
    
    glUnmapBuffer(GL_PIXEL_PACK_BUFFER)
    glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)
    glDeleteBuffers(1, [pixelBuffer])


def initGLUT():
    glutInit()
    glutInitWindowSize(*WINDOW_SIZE)
    glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE|GLUT_DEPTH)
    glutCreateWindow("DroneDeploy - Reconstruction Challenge")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMotionFunc(motion)
    glutMouseFunc(mouse)


def initOpenGL():
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)


app = None
def initApplication():
    if len(sys.argv) != 3:
        raise Exception("Format: python <csvFile> <imagesLocation>")

    global app
    app = Application(sys.argv[1], sys.argv[2])


def main():
    initGLUT()
    initOpenGL()
    initApplication()

    return glutMainLoop()


if __name__ == "__main__":
    main()

