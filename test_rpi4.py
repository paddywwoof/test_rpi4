from ctypes import POINTER, c_int, c_uint, c_float, c_char, c_char_p, byref, CDLL
from ctypes.util import find_library
import numpy as np
import time

import sdl2
import sdl2.ext
import sdl2.video

from test_rpi4_constants import *

W, H = 500, 300
DRAW_METHODS = [GL_TRIANGLES, GL_POINTS, GL_LINE_LOOP, GL_LINE_STRIP, GL_LINES]
USE_ES = False

if not USE_ES:
  opengles = CDLL(find_library('GL'))
else:
  opengles = CDLL(find_library('GLESv2')) # has to happen first
openegl = CDLL(find_library('EGL')) # otherwise missing symbol on pi loading egl

set_gles_function_args(opengles)
set_egl_function_args(openegl)

''' SDL2 window stuff
'''
flags = sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE
stat = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO, flags)
assert (stat == 0), 'failed to init sdl2: {}'.format(sdl2.SDL_GetError())
mode = sdl2.SDL_DisplayMode()
sdl2.SDL_GetCurrentDisplayMode(0, byref(mode))
flags = sdl2.SDL_WINDOW_OPENGL
window = sdl2.SDL_CreateWindow(b'hello world',
                              0, 0, W, H,
                              flags)
assert window, sdl2.SDL_GetError()
# Force OpenGL 2.1 'core' context. Must set *before* creating GL context!
sdl2.video.SDL_GL_SetAttribute(sdl2.video.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
sdl2.video.SDL_GL_SetAttribute(sdl2.video.SDL_GL_CONTEXT_MINOR_VERSION, 1)
sdl2.video.SDL_GL_SetAttribute(sdl2.video.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.video.SDL_GL_CONTEXT_PROFILE_CORE)
context = sdl2.SDL_GL_CreateContext(window)

''' gl stuff
'''
opengles.glViewport(0, 0, W, H)
opengles.glDepthRangef(c_float(0.0), c_float(1.0))
opengles.glClearColor (c_float(0.3), c_float(0.3), c_float(0.7), c_float(1.0))
opengles.glBindFramebuffer(GL_FRAMEBUFFER, 0)

#Setup default hints
opengles.glEnable(GL_CULL_FACE)
opengles.glEnable(GL_DEPTH_TEST)
opengles.glEnable(GL_PROGRAM_POINT_SIZE)
opengles.glDepthFunc(GL_LESS)
opengles.glDepthMask(1)
opengles.glCullFace(GL_FRONT)
opengles.glHint(GL_GENERATE_MIPMAP_HINT, GL_NICEST)
opengles.glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, 
                                        1, GL_ONE_MINUS_SRC_ALPHA)
opengles.glColorMask(1, 1, 1, 0)
if not USE_ES:
  opengles.glPointSize(c_float(20.0))
opengles.glLineWidth(c_float(2.0))

array_buffer = np.array([-0.5, -0.5, 0.5, 1.0, 0.0, 0.0, # vertex x,y,z,r,g,b
                         -0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
                         0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
                         0.5, -0.5, 0.5, 1.0, 1.0, 1.0], dtype="float32")
vbuf = c_uint()
opengles.glGenBuffers(1, byref(vbuf))
opengles.glBindBuffer(GL_ARRAY_BUFFER, vbuf)
opengles.glBufferData(GL_ARRAY_BUFFER,
                      array_buffer.nbytes,
                      array_buffer.ctypes.data_as(POINTER(c_float)),
                      GL_STATIC_DRAW)

element_array_buffer = np.array([0, 1, 2, 0, 2, 3], dtype="short")
ebuf = c_uint()
opengles.glGenBuffers(1, byref(ebuf))
opengles.glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebuf)
opengles.glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                      element_array_buffer.nbytes,
                      element_array_buffer.ctypes.data_as(POINTER(c_float)),
                      GL_STATIC_DRAW)

program = opengles.glCreateProgram()
vsrc = b'''attribute vec3 vert;
attribute vec3 rgb;
varying vec4 colour;
void main(void) {
  colour = vec4(rgb, 1.0);
  gl_Position = vec4(vert, 1.0);
  gl_PointSize = 20.0;
} 
'''
vshader = opengles.glCreateShader(GL_VERTEX_SHADER)
src_len = c_int(len(vsrc))
opengles.glShaderSource(vshader, 1, c_char_p(vsrc), byref(src_len))
opengles.glCompileShader(vshader)
opengles.glAttachShader(program, vshader)

fsrc = b'''varying vec4 colour;
void main(void) {
  gl_FragColor = colour;
}
'''
fshader = opengles.glCreateShader(GL_FRAGMENT_SHADER)
src_len = c_int(len(fsrc))
opengles.glShaderSource(fshader, 1, c_char_p(fsrc), byref(src_len))
opengles.glCompileShader(fshader)
opengles.glAttachShader(program, fshader)

opengles.glLinkProgram(program)
opengles.glUseProgram(program)

attr_vert = opengles.glGetAttribLocation(program, b'vert')
attr_rgb = opengles.glGetAttribLocation(program, b'rgb')

for i in range(20):
  time.sleep(0.5)
  opengles.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  opengles.glBindBuffer(GL_ARRAY_BUFFER, vbuf)
  opengles.glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebuf)
  opengles.glVertexAttribPointer(attr_vert, 3, GL_FLOAT, 0, 24, 0)
  opengles.glEnableVertexAttribArray(attr_vert)
  opengles.glVertexAttribPointer(attr_rgb, 3, GL_FLOAT, 0, 24, 12)
  opengles.glEnableVertexAttribArray(attr_rgb)
  opengles.glDrawElements(DRAW_METHODS[i%5], 6, GL_UNSIGNED_SHORT, 0)
  sdl2.SDL_GL_SwapWindow(window)

sdl2.SDL_GL_DeleteContext(context)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()
