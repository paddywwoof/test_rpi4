from ctypes import (POINTER, c_void_p, c_int, c_uint, c_int8, c_uint8, c_int16, c_uint16,
        c_int32, c_uint32, c_int64, c_uint64, c_float, c_double, c_char, c_char_p,
        c_ubyte, c_long, c_ulong, c_short, c_ushort, c_byte, Structure, byref, sizeof)

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
GL_VERTEX_ARRAY = 0x8074

GLboolean = c_uint8
GLbyte =  c_int8
GLubyte =  c_uint8
GLshort = c_int16
GLushort = c_uint16
GLint = c_int32
GLuint =  c_uint32
#GLfixed 32 Signed, 2's complement 16.16 integer GL_FIXED
GLint64 =  c_int64
GLuint64 =  c_uint64
GLsizei =  c_uint32
GLenum =  c_uint32
bits32 = (sizeof(c_void_p()) == 4) # 32 bits in 4 bytes
GLintptr = c_int32 if bits32 else c_int64
GLsizeiptr  = c_uint32 if bits32 else c_uint64
GLsync  = c_uint32 if bits32 else c_uint64
GLbitfield = c_uint32
#GLhalf 16 An IEEE-754 floating-point value GL_HALF_FLOAT
GLfloat = c_float
GLclampf = c_float
GLdouble = c_double
GLclampd = c_double

def set_gles_function_args(gles):
  gles.glAttachShader.argtypes = [GLuint, GLuint]
  gles.glAttachShader.restype = None
  gles.glBindBuffer.argtypes = [GLenum, GLuint]
  gles.glBindBuffer.restype = None
  gles.glBindFramebuffer.argtypes = [GLenum, GLuint]
  gles.glBindFramebuffer.restype = None
  gles.glBlendFuncSeparate.argtypes = [GLenum, GLenum, GLenum, GLenum]
  gles.glBlendFuncSeparate.restype = None
  gles.glBufferData.argtypes = [GLenum, GLsizeiptr, c_void_p, GLenum]
  gles.glBufferData.restype = None
  gles.glClearColor.argtypes = [GLclampf, GLclampf, GLclampf, GLclampf]
  gles.glClearColor.restype = None
  gles.glColorMask.argtypes = [GLboolean, GLboolean, GLboolean, GLboolean]
  gles.glColorMask.restype = None
  gles.glCompileShader.argtypes = [GLuint]
  gles.glCompileShader.restype = None
  gles.glCreateProgram.argtypes = [] # void
  gles.glCreateProgram.restype = GLuint
  gles.glCreateShader.argtypes = [GLenum]
  gles.glCreateShader.restype = GLuint
  gles.glCullFace.argtypes = [GLenum]
  gles.glCullFace.restype = None
  gles.glDepthFunc.argtypes = [GLenum]
  gles.glDepthFunc.restype = None
  gles.glDepthMask.argtypes = [GLboolean]
  gles.glDepthMask.restype = None
  gles.glDepthRange.argtypes = [GLclampd, GLclampd] # NB not in ES
  gles.glDepthRange.restype = None
  gles.glDepthRangef.argtypes = [GLclampf, GLclampf] # NB not in GL < 4
  gles.glDepthRangef.restype = None
  gles.glDrawElements.argtypes = [GLenum, GLsizei, GLenum, c_void_p]
  gles.glDrawElements.restype = None

  
  gles.glEnable.argtypes = [GLenum]
  gles.glEnable.restype = None
  gles.glEnableClientState.argtypes = [GLenum]
  gles.glEnableClientState.restype = None
  gles.glEnableVertexAttribArray.argtypes = [GLuint]
  gles.glEnableVertexAttribArray.restype = None
  gles.glGenBuffers.argtypes = [GLsizei, POINTER(GLuint)]
  gles.glGenBuffers.restype = None
  gles.glGetAttribLocation.argtypes = [GLuint, POINTER(c_char)]
  gles.glGetAttribLocation.restype = GLint
  gles.glHint.argtypes = [GLenum, GLenum]
  gles.glHint.restype = None
  gles.glLineWidth.argtypes = [GLfloat]
  gles.glLineWidth.restype = None
  gles.glLinkProgram.argtypes = [GLuint]
  gles.glLinkProgram.restype = None
  gles.glPointSize.argtypes = [GLfloat]
  gles.glPointSize.restype = None
  gles.glShaderSource.argtypes = [GLuint, GLsizei, POINTER(c_char_p), POINTER(GLint)]
  gles.glShaderSource.restype = None
  gles.glUseProgram.argtypes = [GLuint]
  gles.glUseProgram.restype = None
  gles.glVertexAttribPointer.argtypes = [GLuint, GLint, GLenum, GLboolean, GLsizei, c_void_p]
  gles.glVertexAttribPointer.restype = None
  gles.glViewport.argtypes = [GLint, GLint, GLsizei, GLsizei]
  gles.glViewport.restype = None
