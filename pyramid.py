#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 18:20:00 2016

@author: Leonardo Nascimento
"""

import shader

import numpy as np
import matrix as mat

from OpenGL.GL import *


vertexShaderSource = """
    #version 330 core
    
    in vec3 a_position;
    in vec4 a_color;

    out vec4 v_color;
    
    uniform mat4 u_model;
    uniform mat4 u_view;
    uniform mat4 u_projection;

    void main()
    {
        gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0f);
        v_color = a_color;
    }
"""


fragmentShaderSource = """
    #version 330 core

    in vec4 v_color;

    out vec4 f_color;

    uniform vec4 u_colormod;

    void main()
    {
        f_color = v_color - u_colormod;
    } 
"""    


class Pyramid:
    def __init__(self, position, rectangle):
        self.initShaderProgram()
        self.initVertexArrayObject(position, rectangle)


    def draw(self, width, height, z, full):
        glUseProgram(self.shaderProgram)
        glUniformMatrix4fv(self.locations["u_model"], 1, GL_TRUE, np.eye(4))
        glUniformMatrix4fv(self.locations["u_view"], 1, GL_TRUE, mat.translation(np.array([0.0, 0.0, -z], np.float32)))
        glUniformMatrix4fv(self.locations["u_projection"], 1, GL_TRUE, mat.perspective(45.0, float(width)/float(height), 0.1, 1000.0))
        glUniform4f(self.locations["u_colormod"], *(np.zeros(4)) if not full else (np.array([0.0, 0.0, 1.0, 0.0], np.float32)))
        glBindVertexArray(self.vertexArrayObject)
        glDrawElements(GL_LINES, 24 if full else 8, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)


    def initVertexArrayObject(self, p, rect):
        vertexData = np.zeros(5, [("vertices", np.float32, 3), ("colors", np.float32, 4)])
        vertexData['vertices'] = [p, rect.bottomLeft, rect.topLeft, rect.topRight, rect.bottomRight]
        vertexData['colors'] = [(1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0)]
        indices = np.array([(1, 2), (2, 3), (3, 4), (4, 1), (0, 1), (1, 2),(0, 2), (2, 3), (0, 3), (3, 4), (0, 4), (4, 1)], np.uint32)
        self.vertexArrayObject = glGenVertexArrays(1)
        glBindVertexArray(self.vertexArrayObject)
        for attrib in self.attribs:
            glEnableVertexAttribArray(self.locations[attrib])
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, vertexData, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        glVertexAttribPointer(self.locations["a_position"], 3, GL_FLOAT, GL_FALSE, vertexData.strides[0], ctypes.c_void_p(0))
        glVertexAttribPointer(self.locations["a_color"], 3, GL_FLOAT, GL_FALSE, vertexData.strides[0], ctypes.c_void_p(vertexData.dtype["vertices"].itemsize))
        glBindVertexArray(0)


    def initShaderProgram(self):
        self.attribs = ["a_position", "a_color"]
        self.uniforms = ["u_model", "u_view", "u_projection", "u_colormod"]
        self.locations = dict((k, v) for (v, k) in enumerate(self.attribs))
        vertexShader = shader.createShader(GL_VERTEX_SHADER, vertexShaderSource)
        fragmentShader = shader.createShader(GL_FRAGMENT_SHADER, fragmentShaderSource)
        self.shaderProgram = glCreateProgram()
        glAttachShader(self.shaderProgram, vertexShader)
        glAttachShader(self.shaderProgram, fragmentShader)
        glLinkProgram(self.shaderProgram)
        if glGetProgramiv(self.shaderProgram, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.shaderProgram))
        for attrib in self.attribs:
            glBindAttribLocation(self.shaderProgram, self.locations[attrib], attrib)
        for uniform in self.uniforms:
            self.locations[uniform] = glGetUniformLocation(self.shaderProgram, uniform)
        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)







