from math3d import *

from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from math import pi
import numpy
import sys, re, traceback

_near = 0.01
_far = 100.0

_varLine = r'^slidable_(\w+)(\s*)=(\s*)([-0-9.]+)(\s*#\s*([-0-9.]+)\s*([-0-9.]+)$)?'

_startText = """

import numpy

slidable_alpha = 4.5 # 0.1 5

slidable_beta = 4.5 # 0.1 5

polyhedra = [ Polyhedron(
    [ numpy.array([ 1, 1, 1]),
      numpy.array([ 1, 1,-1]),
      numpy.array([ 1,-1, 1]),
      numpy.array([ 1,-1,-1]),
      numpy.array([-1, 1, 1]),
      numpy.array([-1, 1,-1]),
      numpy.array([-1,-1, 1]),
      numpy.array([-1,-1,-1]) ],
    [ (2, 3, 1, 0),
      (4, 5, 7, 6),
      (0, 1, 5, 4),
      (6, 7, 3, 2),
      (4, 6, 2, 0),
      (1, 3, 7, 5)
      ])
]

"""

_filePath = None

class GlWidget(QtOpenGL.QGLWidget):

    def __init__(self):
        super().__init__()
        self.polyhedra = []

        self.lastPos = (0, 0)
        self.xRot = 0.0
        self.yRot = 0.0

        self.center = numpy.array([0.0,0.0,0.0])

        self.distance = 2.0

    def minimumSizeHint(self):
        return QtCore.QSize(100, 300)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def mousePressEvent(self, event):
        self.lastPos = (event.x(), event.y())

        if event.buttons() == QtCore.Qt.RightButton:
            self.makeCurrent()

            dummyX, dummyY, vWidth, vHeight = glGetFloatv(GL_VIEWPORT)
            xSample = int(event.x() * vWidth / self.width())
            ySample = vHeight - int(event.y() * vHeight / self.height())

            zSample = glReadPixels(xSample, ySample,
                                   1, 1,
                                   GL_DEPTH_COMPONENT,
                                   GL_FLOAT)

            zSample = zSample[0,0]

            zSample = 2 * zSample - 1.0

            if zSample > 0.9999 or zSample < -0.9999:
                return

            x = -1.0 + float(event.x() / self.width()) * 2.0
            y = +1.0 - float(event.y() / self.height()) * 2.0
            
            modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
            proj = glGetFloatv(GL_PROJECTION_MATRIX)
            p = numpy.linalg.inv(modelview.dot(proj))

            v = numpy.array([x,y,zSample,1]).dot(p)

            self.center = v[0:3] / v[3]

            self.repaint()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos[0]
        dy = event.y() - self.lastPos[1]

        if event.buttons() == QtCore.Qt.LeftButton:
            self.xRot += dx
            self.yRot += dy
            self.repaint()

        self.lastPos = (event.x(), event.y())

    def paintEvent(self, e):

        painter = QtGui.QPainter(self)

        painter.beginNativePainting()

        glClearColor (0.0, 0.0, 0.0, 0.0);

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, float(self.width()) / self.height(), _near, _far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glLightfv(GL_LIGHT0, GL_DIFFUSE, [ 1.0, 1.0, 1.0, 1.0 ])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [ 1.0, 1.0, 1.0, 1.0 ])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [ 0.1, 0.1, 0.1, 1.0 ])
        glLightfv(GL_LIGHT0, GL_POSITION, [ 0.0, 3.0, 2.0, 1.0 ])

        glLightfv(GL_LIGHT1, GL_DIFFUSE, [ 1.0, 1.0, 1.0, 1.0 ])
        glLightfv(GL_LIGHT1, GL_SPECULAR, [ 1.0, 1.0, 1.0, 1.0 ])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [ 0.1, 0.1, 0.1, 1.0 ])
        glLightfv(GL_LIGHT1, GL_POSITION, [ 0.0, -3.0, 2.0, 1.0 ])


        glTranslatef(0, 0, -self.distance)
        glRotatef(self.yRot, 1.0, 0.0, 0.0)
        glRotatef(self.xRot, 0.0, 1.0, 0.0)
        glRotatef(-90, 1.0, 0.0, 0.0)
        glTranslatef(*-self.center)


        glEnable(GL_LIGHTING);
        glEnable(GL_LIGHT0);
        glEnable(GL_LIGHT1);
        glEnable(GL_DEPTH_TEST);

        glShadeModel(GL_SMOOTH)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.5, 0.1, 0.1, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.1, 0.1, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])

        glEnable(GL_NORMALIZE)

        for polyhedron in self.polyhedra:
            for vertices, normal in polyhedron.facesWithNormal():
                ambient = [ polyhedron.color[0] * 0.5,
                            polyhedron.color[1] * 0.5,
                            polyhedron.color[2] * 0.5,
                            1.0 ]
                diffuse = [ polyhedron.color[0],
                            polyhedron.color[1],
                            polyhedron.color[2],
                            1.0 ]

                glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
                glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)


                glBegin(GL_TRIANGLE_FAN)
                
                glNormal3f(*normal)
                for vertex in vertices:
                    glVertex3f(*vertex)

                glEnd()

        glDisable(GL_LIGHTING);
        glDisable(GL_LIGHT0);
        glDisable(GL_LIGHT1);
        glDisable(GL_DEPTH_TEST);
        
        painter.endNativePainting()

        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        proj = glGetFloatv(GL_PROJECTION_MATRIX)

        for polyhedron in self.polyhedra:
            if polyhedron.labels:
                for label, vertex in zip(polyhedron.labels, polyhedron.vertices):
                    p = numpy.array([vertex[0], vertex[1], vertex[2], 1.0]).dot(modelview.dot(proj))
                
                    x = self.width() * (1 + p[0] / p[3]) / 2.0
                    y = self.height() * (1 - p[1] / p[3]) / 2.0

                    l = label
                    if polyhedron.name:
                        l += ' (%s)' % polyhedron.name
                    
                    painter.setPen(QtCore.Qt.white)
                    painter.setFont(QtGui.QFont("Arial", 16))
                    painter.drawText(x, y - 10, 100, 20,
                                     QtCore.Qt.AlignLeft,
                                     l)

        painter.end()

class MainWindow(QtWidgets.QWidget):

    def distanceSlider(self, value):
        self.glWidget.distance = value / 10.0
        self.glWidget.repaint()
            


    def __init__(self):
        super().__init__()

        self.mlayout = QtWidgets.QHBoxLayout(self)
        self.layout = QtWidgets.QSplitter()
        self.mlayout.addWidget(self.layout)

        self.graphicsPanel = QtWidgets.QWidget()
        self.layout.addWidget(self.graphicsPanel)
        
        self.graphicsLayout = QtWidgets.QVBoxLayout(self.graphicsPanel)

        self.sizeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sizeSlider.setMinimum(0)
        self.sizeSlider.setMaximum(100)
        self.sizeSlider.setValue(50)
        self.graphicsLayout.addWidget(self.sizeSlider)

        self.glWidget = GlWidget()
        self.graphicsLayout.addWidget(self.glWidget)

        self.sizeSlider.valueChanged.connect(self.distanceSlider)

        self.textPanel = QtWidgets.QWidget()
        self.textPanelLayout = QtWidgets.QVBoxLayout(self.textPanel)

        self.sliderContainer = QtWidgets.QWidget()
        self.sliderLayout = QtWidgets.QGridLayout(self.sliderContainer)
        self.textPanelLayout.addWidget(self.sliderContainer)

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setCurrentFont(
            QtGui.QFontDatabase.systemFont(
                QtGui.QFontDatabase.FixedFont))

        self.textEdit.setText(_startText)

        self.textPanelLayout.addWidget(self.textEdit)

        self.runSaveButtonLayout = QtWidgets.QHBoxLayout()
        self.textPanelLayout.addLayout(self.runSaveButtonLayout)

        self.runButton = QtWidgets.QPushButton("Run")
        self.runButton.clicked.connect(self.run)
        self.runSaveButtonLayout.addWidget(self.runButton)
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        self.runSaveButtonLayout.addWidget(self.saveButton)
        self.reloadButton = QtWidgets.QPushButton("Reload")
        self.reloadButton.clicked.connect(self.reload)
        self.runSaveButtonLayout.addWidget(self.reloadButton)

        self.layout.addWidget(self.textPanel)

        self.updateSlidersFromText()

    def save(self):
        text = self.textEdit.toPlainText()

        global _filePath

        open(_filePath, 'w').write(text)
        
    def reload(self):
        global _filePath

        print("Reloading", _filePath)

        t = open(_filePath, 'r').read()

        self.textEdit.setText(t)
        self.lines = t.split('\n')

        self.execute()
        

    def setVar(self, value, lineNumber, data):
        varName, white1, white2, valStr, rangeStr, minStr, maxStr = data
        
        minVal = float(minStr)
        maxVal = float(maxStr)

        val = minVal + (maxVal - minVal) * value / 1000.0

        self.lines[lineNumber] = 'slidable_%s%s=%s%f%s' % (
            varName, white1, white2, val, rangeStr)

        self.textEdit.setText('\n'.join(self.lines))

        self.execute()

    def run(self):
        self.updateSlidersFromText()
        self.execute()
        
    def execute(self):
        text = self.textEdit.toPlainText()

        l = {}
        try:
            exec(text, globals(), l)
        except Exception as e:
            t, ex, tb = sys.exc_info()
            print(t)
            print(ex)
            print(traceback.format_tb(tb))

        self.glWidget.polyhedra = l.get('polyhedra', [])
        self.glWidget.repaint()

    def updateSlidersFromText(self):
        for i in range(0, self.sliderLayout.rowCount()):
            for j in range(2):
                item = self.sliderLayout.itemAtPosition(i, j)
                if item:
                    item.widget().deleteLater()

        text = self.textEdit.toPlainText()

        i = 0

        self.lines = text.split('\n')
        for lineNumber, line in enumerate(self.lines):
            m = re.match(_varLine, line)
            if m:
                data = m.groups()
                varName, white1, white2, valStr, rangeStr, minStr, maxStr = data

                label = QtWidgets.QLabel(varName)
                self.sliderLayout.addWidget(label, i, 0)

                slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(1000)
                minVal = float(minStr)
                maxVal = float(maxStr)
                val = float(valStr)

                slider.setValue(
                    (val - minVal) / (maxVal - minVal) * 1000.0)
                
                slider.valueChanged.connect(
                    lambda value,
                    lineNumber = lineNumber,
                    data = data : self.setVar(
                        value, lineNumber, data))
                self.sliderLayout.addWidget(slider, i, 1)

                i += 1


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    if len(sys.argv) > 1:
        _filePath = sys.argv[-1]
        _startText = open(_filePath).read()

    m = MainWindow()
    m.show()
    m.execute()

    sys.exit(app.exec_())

