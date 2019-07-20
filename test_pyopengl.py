#!/usr/bin/env python
# The MIT License (MIT)
#
# Copyright (c) 2014 Richard Hawkins
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
''' modified quite a bit by Paddy Gaunt 19Jul2019. See
 https://gist.github.com/hurricanerix/3be8221128d943ae2827 for original
 
 any key toggle lines, triangles, points
 mouse click toggle glDrawElements, glDrawArrays
'''
import ctypes
import numpy as np
import sys

import sdl2
from OpenGL import GL as gl
from OpenGL.GL import shaders

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
VERT_SOURCE = b"""
uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 proj_matrix;
attribute vec3 mc_vertex;
attribute vec3 mc_colour;
varying vec4 colour;
void main()
{
  mat4 mv_matrix = view_matrix * model_matrix;
  vec4 cc_vertex = mv_matrix * vec4(mc_vertex, 1.0);
  colour = vec4(mc_colour, 1.0);
  gl_Position = proj_matrix * cc_vertex;
}"""
FRAG_SOURCE = b"""
varying vec4 colour;
void main()
{
    gl_FragColor = colour;
}"""

VERTICES = np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                     1.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                     1.0, 1.0, 0.0, 0.0, 0.0, 1.0, # subtle diff c.f. vert[5] to see array v. elements
                     0.0, 1.0, 0.0, 0.5, 0.5, 0.5, 
                     0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                     1.0, 1.0, 0.0, 0.1, 0.1, 0.9], dtype=np.float32)

ELEMENTS = np.array([0, 1, 2, 3, 0, 2], dtype=np.int16)

def get_4x4_transform(scale_x, scale_y, trans_x, trans_y, trans_z):
    transform = np.array([scale_x, 0.0, 0.0, trans_x,
                          0.0, scale_y, 0.0, trans_y,
                          0.0, 0.0, 1.0, trans_z,
                          0.0, 0.0, 0.0, 1.0], dtype=np.float)
    return transform


def _get_projection_matrix(left, right, bottom, top):
    zNear = -25.0
    zFar = 25.0
    inv_z = 1.0 / (zFar - zNear)
    inv_y = 1.0 / (top - bottom)
    inv_x = 1.0 / (right - left)
    mat = np.array([2.0 * inv_x, 0.0, 0.0, -(right + left) * inv_x,
                    0.0, 2.0 * inv_y, 0.0, -(top + bottom) * inv_y,
                    0.0, 0.0, -2.0 * inv_z, -(zFar + zNear) * inv_z,
                    0.0, 0.0, 0.0, 1.0], dtype=np.float)
    return mat

def _get_view_matrix(x, y):
    scale_x = 1.0
    scale_y = 1.0
    trans_x = x
    trans_y = y
    layer = 1.0
    return get_4x4_transform(scale_x, scale_y, trans_x, trans_y, layer)


if __name__ == "__main__":
    # Init
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 0)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,
                             sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
    sdl2.SDL_GL_SetSwapInterval(1)
    window = sdl2.SDL_CreateWindow(
        b"Python/SDL2/OpenGL", sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT,
        sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)
    if not window:
        sys.stderr.write("Error: Could not create window\n")
        exit(1)
    glcontext = sdl2.SDL_GL_CreateContext(window)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_BLEND)
    gl.glPointSize(4.0)
    gl.glClearColor(0.3, 0.3, 0.3, 1.0)

    # Load Shader
    attrib_locs = {
        b"mc_vertex": -1,
    }
    uniform_locs = {
        b"model_matrix": -1,
        b"view_matrix":  -1,
        b"proj_matrix":  -1,
    }
    vert_prog = shaders.compileShader(VERT_SOURCE, gl.GL_VERTEX_SHADER)
    if not gl.glGetShaderiv(vert_prog, gl.GL_COMPILE_STATUS):
        sys.stderr.write("Error: Could not compile vertex shader.\n")
        exit(2)
    frag_prog = shaders.compileShader(FRAG_SOURCE, gl.GL_FRAGMENT_SHADER)
    if not gl.glGetShaderiv(frag_prog, gl.GL_COMPILE_STATUS):
        sys.stderr.write("Error: Could not compile fragment shader.\n")
        exit(3)
    shader = gl.glCreateProgram()
    gl.glAttachShader(shader, vert_prog)
    gl.glAttachShader(shader, frag_prog)
    gl.glLinkProgram(shader)
    if gl.glGetProgramiv(shader, gl.GL_LINK_STATUS) != gl.GL_TRUE:
        sys.stderr.write("Error: {0}\n".format(gl.glGetProgramInfoLog(shader)))
        exit(4)
    for name in [b'mc_vertex', b'mc_colour']:
        attrib_locs[name] = gl.glGetAttribLocation(shader, name)
    for name in [b'model_matrix', b'view_matrix', b'proj_matrix']:
        uniform_locs[name] = gl.glGetUniformLocation(shader, name)

    # Load Object
    vertex_buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, VERTICES.nbytes, VERTICES,
                    gl.GL_STATIC_DRAW)
    element_buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, element_buffer)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, ELEMENTS.nbytes, ELEMENTS,
                    gl.GL_STATIC_DRAW)
    gl.glVertexAttribPointer(attrib_locs[b'mc_vertex'], 3, gl.GL_FLOAT, False,
                             24, ctypes.c_void_p(0))
    gl.glVertexAttribPointer(attrib_locs[b'mc_colour'], 3, gl.GL_FLOAT, False,
                             24, ctypes.c_void_p(12))
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    #gl.glBindVertexArray(0)

    # Loop
    running = True
    event = sdl2.SDL_Event()
    object_w = 200
    object_h = 200
    i = 0
    d_type = [gl.GL_POINTS, gl.GL_TRIANGLES, gl.GL_LINES, gl.GL_LINE_LOOP]
    use_arrays = False
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False
            if event.type == sdl2.events.SDL_KEYDOWN:
                #print("SDL_KEYDOWN")
                i += 1
                if i >= len(d_type):
                  i = 0
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
            if (event.type == sdl2.SDL_MOUSEMOTION):
                #print("SDL_MOUSEMOTION")
                object_w = event.motion.x * 0.2 + 200
                object_h = event.motion.y * 0.2 + 200
                gl.glPointSize(object_w * 0.05)
                gl.glLineWidth(object_h * 0.05)
            if (event.type == sdl2.SDL_MOUSEBUTTONDOWN):
                #print("SDL_MOUSEBUTTONDOWN")
                use_arrays = not use_arrays

        # Update model_matrix
        object_x = WINDOW_WIDTH / 2 - object_w / 2
        object_y = WINDOW_HEIGHT / 2 - object_h / 2
        model_matrix = get_4x4_transform(scale_x=object_w, scale_y=object_h,
                                         trans_x=object_x, trans_y=object_y,
                                         trans_z=1.0)
        # Update proj_matrix
        proj_matrix = _get_projection_matrix(0.0, WINDOW_WIDTH,
                                             0.0, WINDOW_HEIGHT)
        # Update view_matrix
        view_matrix = _get_view_matrix(1.0, 1.0)

        # Start Rendering
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glUseProgram(shader)
    
        # Draw object
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, element_buffer)
        gl.glEnableVertexAttribArray(attrib_locs[b'mc_vertex'])
        gl.glEnableVertexAttribArray(attrib_locs[b'mc_colour'])
        gl.glUniformMatrix4fv(uniform_locs[b'model_matrix'], 1, gl.GL_TRUE,
                              model_matrix)
        gl.glUniformMatrix4fv(uniform_locs[b'view_matrix'], 1, gl.GL_TRUE,
                              view_matrix)
        gl.glUniformMatrix4fv(uniform_locs[b'proj_matrix'], 1, gl.GL_TRUE,
                              proj_matrix)
        if use_arrays: # toggle with mouse click. Any key change points, triangles, lines
            gl.glDrawArrays(d_type[i], 0, int(len(VERTICES) / 6.0))
        else:
            gl.glDrawElements(d_type[i], len(ELEMENTS), gl.GL_UNSIGNED_SHORT, None)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

        # Stop Rendering
        gl.glUseProgram(0)
        sdl2.SDL_GL_SwapWindow(window)

sdl2.SDL_GL_DeleteContext(glcontext)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()
