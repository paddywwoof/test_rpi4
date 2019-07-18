from ctypes import (POINTER, c_void_p, c_int, c_int32, c_uint, c_float, c_char, c_char_p, c_ubyte,
                    c_long, c_ulong, c_short, c_ushort, c_byte, Structure, byref)

EGL_DEFAULT_DISPLAY = 0
EGL_BLUE_SIZE = 0x3022
EGL_GREEN_SIZE = 0x3023
EGL_RED_SIZE = 0x3024
EGL_BUFFER_SIZE = 0x3020
EGL_ALPHA_SIZE = 0x3021
EGL_DEPTH_SIZE = 0x3025
EGL_SAMPLES = 0x3031
EGL_STENCIL_SIZE = 0x3026
EGL_SURFACE_TYPE = 0x3033
EGL_WINDOW_BIT = 0x0004
EGL_NONE = 0x3038
EGL_CONTEXT_CLIENT_VERSION = 0x3098
EGL_NO_CONTEXT = 0
KEY_PRESS_MASK = (1<<0)
KEY_RELEASE_MASK = (1<<1)
GL_FRAMEBUFFER = 0x8D40
GL_CULL_FACE = 0x0B44
GL_DEPTH_TEST = 0x0B71
GL_LESS = 0x0201
GL_FRONT = 0x0404
GL_NICEST = 0x1102
GL_GENERATE_MIPMAP_HINT = 0x8192
GL_SRC_ALPHA = 0x0302
GL_ONE_MINUS_SRC_ALPHA = 0x0303
GL_COLOR_BUFFER_BIT = 0x00004000
GL_DEPTH_BUFFER_BIT = 0x00000100
GL_ARRAY_BUFFER = 0x8892
GL_ELEMENT_ARRAY_BUFFER = 0x8893
GL_STATIC_DRAW = 0x88E4
GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER = 0x8B31
GL_UNSIGNED_SHORT = 0x1403
GL_INT = 0x1404
GL_UNSIGNED_INT = 0x1405
GL_FLOAT = 0x1406
GL_POINTS = 0x0000
GL_LINES = 0x0001
GL_LINE_LOOP = 0x0002
GL_LINE_STRIP = 0x0003
GL_TRIANGLES = 0x0004
GL_PROGRAM_POINT_SIZE = 0x8642

def set_gles_function_args(gles):
  gles.glAttachShader.argtypes = [c_uint, c_uint] #GLuint, GLuint
  gles.glBindBuffer.argtypes = [c_uint, c_uint] #GLenum, GLuint
  gles.glBindFramebuffer.argtypes = [c_uint, c_uint] #GLenum, GLuint 
  gles.glBlendFuncSeparate.argtypes = [c_uint, c_uint, c_uint, c_uint] #GLenum, GLenum, GLenum, GLenum
  gles.glBufferData.argtypes = [c_uint, c_int, c_void_p, c_uint] #GLenum, GLsizeiptr, const GLvoid *, GLenum
  gles.glClearColor.argtypes = [c_float, c_float, c_float, c_float] #GLclampf, GLclampf, GLclampf, GLclampf 
  gles.glColorMask.argtypes = [c_ubyte, c_ubyte, c_ubyte, c_ubyte] #GLboolean, GLboolean, GLboolean blue, GLboolean
  gles.glCompileShader.argtypes = [c_uint] # GLuint
  gles.glCreateProgram.argtypes = [] # void
  gles.glCreateProgram.restype = c_uint
  gles.glCreateShader.argtypes = [c_uint] #GLenum
  gles.glCreateShader.restype = c_uint
  gles.glCullFace.argtypes = [c_uint] #GLenum
  gles.glDepthFunc.argtypes = [c_uint] #GLenum
  gles.glDepthMask.argtypes = [c_ubyte] #GLboolean 
  gles.glDepthRangef.argtypes = [c_float, c_float] #GLclampf, GLclampf 
  gles.glDrawElements.argtypes = [c_uint, c_int, c_uint, c_void_p] #GLenum, GLsizei, GLenum, const GLvoid *
  gles.glEnable.argtypes = [c_uint] #GLenum 
  gles.glEnableVertexAttribArray.argtypes = [c_uint] #GLuint 
  gles.glGenBuffers.argtypes = [c_int, POINTER(c_uint)] #GLsizei, GLuint *
  gles.glGetAttribLocation.argtypes = [c_uint, POINTER(c_char)] #GLuint, const GLchar *
  gles.glGetAttribLocation.restype = c_int
  gles.glHint.argtypes = [c_uint, c_uint] #GLenum, GLenum
  gles.glLinkProgram.argtypes = [c_uint] #GLuint
  gles.glShaderSource.argtypes = [c_uint, c_int, POINTER(c_char_p), POINTER(c_int)] #GLuint, GLsizei, const GLchar * const *, const GLint *
  gles.glUseProgram.argtypes = [c_int] #GLuint
  gles.glVertexAttribPointer.argtypes = [c_uint, c_int, c_uint, c_ubyte, c_int, c_void_p] #GLuint, GLint, GLenum, GLboolean, GLsizei, const GLvoid * 
  gles.glViewport.argtypes = [c_int, c_int, c_int, c_int] #GLint, GLint, GLsizei, GLsizei

def set_egl_function_args(egl):
  egl.eglChooseConfig.argtypes = [c_void_p, c_void_p, c_void_p, c_int32, POINTER(c_int32)]
  egl.eglChooseConfig.restype = c_int #EGLBoolean
  egl.eglCreateContext.argtypes = [c_void_p, c_void_p, c_int32, c_void_p]
  egl.eglCreateContext.restype = c_void_p
  egl.eglCreateWindowSurface.argtypes = [c_void_p, c_void_p, c_void_p, c_int32]
  egl.eglCreateWindowSurface.restype = c_void_p
  egl.eglDestroyContext.argtypes = [c_void_p, c_void_p]
  egl.eglDestroySurface.argtypes = [c_void_p, c_void_p]
  egl.eglGetCurrentSurface.argtypes = [c_int32]
  egl.eglGetCurrentSurface.restype = c_void_p
  egl.eglGetDisplay.restype = c_void_p
  egl.eglInitialize.argtypes = [c_void_p, POINTER(c_int32), POINTER(c_int32)]
  egl.eglMakeCurrent.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
  egl.eglSwapBuffers.argtypes = [c_void_p, c_void_p]
  egl.eglQuerySurface.argtypes = [c_void_p, c_void_p, c_int32, POINTER(c_int32)]
  egl.eglTerminate.argtypes = [c_void_p]