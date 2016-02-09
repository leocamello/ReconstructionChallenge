#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 19:15:00 2016

@author: Leonardo Nascimento
"""

import shader

import numpy as np
import matrix as mat

from OpenGL.GL import *


vertexShaderSource = """
    #version 330 core
    
    in vec3 a_position;
    in vec2 a_texCoord;

    out vec2 v_texCoord;
    
    uniform mat4 u_model;
    uniform mat4 u_view;
    uniform mat4 u_projection;

    void main()
    {
        gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0f);
        v_texCoord = a_texCoord;
    }
"""


fragmentShaderSource = """
    #version 330 core

    in vec2 v_texCoord;

    out vec4 f_color;

    uniform sampler2D u_texture;

    void main()
    {
        f_color = texture(u_texture, v_texCoord);
    } 
"""    


class Plane:
    def __init__(self, rectangle, image):
        self.initShaderProgram()
        self.initTexture(image)
        self.initVertexArrayObject(rectangle)


    def draw(self, center, width, height):
        glUseProgram(self.shaderProgram)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(self.locations["u_texture"], 0)
        glUniformMatrix4fv(self.locations["u_model"], 1, GL_TRUE, np.eye(4))
        glUniformMatrix4fv(self.locations["u_view"], 1, GL_TRUE, mat.translation(-center))
        glUniformMatrix4fv(self.locations["u_projection"], 1, GL_TRUE, mat.perspective(45.0, float(width)/float(height), 0.1, 1000.0))
        glBindVertexArray(self.vertexArrayObject)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)


    def initVertexArrayObject(self, rect):
        vertexData = np.zeros(4, [("vertices", np.float32, 3), ("texCoords", np.float32, 2)])
        vertexData['vertices'] = [rect.bottomLeft, rect.topLeft, rect.topRight, rect.bottomRight]
        vertexData['texCoords'] = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
        self.vertexArrayObject = glGenVertexArrays(1)
        glBindVertexArray(self.vertexArrayObject)
        for attrib in self.attribs:
            glEnableVertexAttribArray(self.locations[attrib])
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, vertexData, GL_STATIC_DRAW)
        glVertexAttribPointer(self.locations["a_position"], 3, GL_FLOAT, GL_FALSE, vertexData.strides[0], ctypes.c_void_p(0))
        glVertexAttribPointer(self.locations["a_texCoord"], 2, GL_FLOAT, GL_FALSE, vertexData.strides[0], ctypes.c_void_p(vertexData.dtype["vertices"].itemsize))
        glBindVertexArray(0)


    def initTexture(self, image):
        self.texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, image['width'], image['height'], 0, GL_RGBA, GL_UNSIGNED_BYTE, image['data'])
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)


    def initShaderProgram(self):
        self.attribs = ["a_position", "a_texCoord"]
        self.uniforms = ["u_model", "u_view", "u_projection", "u_texture"]
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







