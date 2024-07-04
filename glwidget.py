import OpenGL.GL as GL
from PyQt6.QtGui import QImage
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtOpenGL import QOpenGLFunctions_4_1_Core, QOpenGLShaderProgram, QOpenGLShader, QOpenGLVertexArrayObject, QOpenGLBuffer, QOpenGLTexture

import numpy as np
import ctypes


class GLWidget(QOpenGLWidget, QOpenGLFunctions_4_1_Core):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gl = QOpenGLFunctions_4_1_Core()

        self.vertices = np.array([
            -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.0, 1.0
        ], dtype=np.float32)
        self.indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype=np.uint32)

        self.program = None
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.texture = None

    def initializeGL(self):
        self.gl.initializeOpenGLFunctions()

        self.program = QOpenGLShaderProgram(self)
        self.vao = QOpenGLVertexArrayObject(self)
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
        self.ebo = QOpenGLBuffer(QOpenGLBuffer.Type.IndexBuffer)

        self.program.create()
        self.program.addShaderFromSourceFile(QOpenGLShader.ShaderTypeBit.Vertex, ':/vertex.glsl')
        self.program.addShaderFromSourceFile(QOpenGLShader.ShaderTypeBit.Fragment, ':/fragment.glsl')
        self.program.link()
        self.program.bind()

        self.vao.create()
        self.vao.bind()

        self.vbo.create()
        self.vbo.bind()
        self.vbo.allocate(self.vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p)).contents, self.vertices.nbytes)

        self.ebo.create()
        self.ebo.bind()
        self.ebo.allocate(self.indices.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p)).contents, self.indices.nbytes)

        self.program.enableAttributeArray(0)
        self.program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 2, 4 * 4)
        self.program.enableAttributeArray(1)
        self.program.setAttributeBuffer(1, GL.GL_FLOAT, 2 * 4, 2, 4 * 4)

        self.texture = QOpenGLTexture(QImage(':/texture.png').mirrored())
        self.texture.setMinificationFilter(QOpenGLTexture.Filter.Linear)
        self.texture.setMagnificationFilter(QOpenGLTexture.Filter.Nearest)
        self.texture.setWrapMode(QOpenGLTexture.WrapMode.Repeat)

    def resizeGL(self, width, height):
        self.gl.glViewport(0, 0, width, height)

    def paintGL(self):
        self.gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.gl.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.program.bind()
        self.texture.bind()
        self.vao.bind()
        self.gl.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)
        self.vao.release()

    def closeEvent(self, event):
        self.makeCurrent()
        self.vbo.destroy()
        self.ebo.destroy()
        self.texture.destroy()
        del self.program
        self.doneCurrent()
        return super().closeEvent(event)
