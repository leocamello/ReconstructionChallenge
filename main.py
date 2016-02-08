#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 14:00:00 2016

@author: Leonardo Nascimento
"""

from OpenGL.GLUT import *
from OpenGL.GL import *

WINDOW_SIZE = 1024, 768

def display():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)


def keyboard(key, x, y):
    if key == '\033':
        sys.exit( )


def motion(x, y):
    pass


def mouse(button, state, x, y):
    pass


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


def main():
    initGLUT()
    initOpenGL()

    return glutMainLoop()


if __name__ == "__main__":
    main()

