"""
Created on Fri Feb 08 18:30:00 2016

@author: Leonardo Nascimento
"""

from OpenGL.GL import *


def createShader(shaderType, shaderSource):
    shader = glCreateShader(shaderType)
    glShaderSource(shader, shaderSource)

    glCompileShader(shader)
    
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))

    return shader