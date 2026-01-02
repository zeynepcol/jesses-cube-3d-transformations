import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *

class CubeGL(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.reset_state()

    def reset_state(self):
        self.tx = self.ty = self.tz = 0.0

        self.angx = self.angy = self.angz = 0.0
        self.px = self.py = self.pz = 0.0
        self.use_arbitrary = False

        self.sx = self.sy = self.sz = 1.0

        self.camera_z = -8.0
        self.last_x = self.last_y = 0

        self.wireframe = False
        self.perspective = True

        self.shear_matrix = [
            1,0,0,0,
            0,1,0,0,
            0,0,1,0,
            0,0,0,1
        ]

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.perspective:
            gluPerspective(45, w / max(h, 1), 1, 100)
        else:
            glOrtho(-5, 5, -5, 5, -20, 20)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(0, 0, self.camera_z)
        glTranslatef(self.tx / 100, self.ty / 100, self.tz / 100)

        glMultMatrixf(self.shear_matrix)

        if self.use_arbitrary:
            glTranslatef(-self.px / 100, -self.py / 100, -self.pz / 100)

        glRotatef(self.angx, 1, 0, 0)
        glRotatef(self.angy, 0, 1, 0)
        glRotatef(self.angz, 0, 0, 1)

        if self.use_arbitrary:
            glTranslatef(self.px / 100, self.py / 100, self.pz / 100)

        glScalef(self.sx, self.sy, self.sz)

        glPolygonMode(GL_FRONT_AND_BACK,
                      GL_LINE if self.wireframe else GL_FILL)

        self.draw_cube()

    def draw_cube(self):
        faces = [
            ((1,0,0), [(1,1,1),(1,-1,1),(1,-1,-1),(1,1,-1)]),
            ((0,1,0), [(-1,1,1),(1,1,1),(1,1,-1),(-1,1,-1)]),
            ((0,0,1), [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]),
            ((1,1,0), [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1)]),
            ((0,1,1), [(-1,-1,1),(-1,-1,-1),(-1,1,-1),(-1,1,1)]),
            ((1,0,1), [(1,-1,1),(1,-1,-1),(1,1,-1),(1,1,1)])
        ]

        glBegin(GL_QUADS)
        for color, face in faces:
            glColor3f(*color)
            for v in face:
                glVertex3f(*v)
        glEnd()

    def mousePressEvent(self, e):
        self.last_x, self.last_y = e.x(), e.y()

    def mouseMoveEvent(self, e):
        dx = e.x() - self.last_x
        dy = e.y() - self.last_y
        self.angy += dx
        self.angx += dy
        self.last_x, self.last_y = e.x(), e.y()
        self.update()

    def wheelEvent(self, e):
        self.camera_z += e.angleDelta().y() / 120
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jesse's Cube")

        layout = QHBoxLayout(self)
        self.gl = CubeGL()

        layout.addLayout(self.controls(), 1)
        layout.addWidget(self.gl, 3)

    def dspin(self):
        s = QDoubleSpinBox()
        s.setRange(-500, 500)
        s.setDecimals(1)
        s.setSingleStep(1)
        return s

    def xyz_row(self, x, y, z):
        row = QHBoxLayout()
        for lbl, box in [("X (px)", x), ("Y (px)", y), ("Z (px)", z)]:
            col = QVBoxLayout()
            col.addWidget(QLabel(lbl))
            col.addWidget(box)
            row.addLayout(col)
        return row

    def controls(self):
        panel = QVBoxLayout()

        title = QLabel("OPTIONS")
        title.setStyleSheet("font-size:20px;font-weight:bold;")
        panel.addWidget(title)
        panel.addWidget(QLabel("Zeynep Çöl"))
        panel.addWidget(QLabel("2025911088"))
        panel.addSpacing(10)

        # Translation
        panel.addWidget(QLabel("Translation"))
        self.tx, self.ty, self.tz = self.dspin(), self.dspin(), self.dspin()
        panel.addLayout(self.xyz_row(self.tx, self.ty, self.tz))
        panel.addWidget(QPushButton("Translate", clicked=self.translate))

        # Rotation
        panel.addWidget(QLabel("Rotation - Angle"))
        self.angx, self.angy, self.angz = self.dspin(), self.dspin(), self.dspin()
        panel.addLayout(self.xyz_row(self.angx, self.angy, self.angz))

        panel.addWidget(QLabel("Rotation - Point"))
        self.px, self.py, self.pz = self.dspin(), self.dspin(), self.dspin()
        panel.addLayout(self.xyz_row(self.px, self.py, self.pz))
        self.arbitrary = QCheckBox("Arbitrary")
        panel.addWidget(self.arbitrary)
        panel.addWidget(QPushButton("Rotate", clicked=self.rotate))

        # Scale
        panel.addWidget(QLabel("Scale"))
        self.sx, self.sy, self.sz = self.dspin(), self.dspin(), self.dspin()
        panel.addLayout(self.xyz_row(self.sx, self.sy, self.sz))
        self.keep_ratio = QCheckBox("Keep Aspect Ratio")
        panel.addWidget(self.keep_ratio)
        panel.addWidget(QPushButton("Scale", clicked=self.scale))

        # Mirror
        panel.addWidget(QLabel("Mirror"))
        mirror_row = QHBoxLayout()
        self.mx, self.my, self.mz = QRadioButton("X"), QRadioButton("Y"), QRadioButton("Z")
        mirror_row.addWidget(self.mx)
        mirror_row.addWidget(self.my)
        mirror_row.addWidget(self.mz)
        panel.addLayout(mirror_row)
        panel.addWidget(QPushButton("Mirror Apply", clicked=self.mirror))

        # Shear
        panel.addWidget(QLabel("Shear"))
        shear_row = QHBoxLayout()
        self.shx, self.shy, self.shz = QRadioButton("X"), QRadioButton("Y"), QRadioButton("Z")
        shear_row.addWidget(self.shx)
        shear_row.addWidget(self.shy)
        shear_row.addWidget(self.shz)
        panel.addLayout(shear_row)
        panel.addWidget(QPushButton("Shear Apply", clicked=self.shear))

        panel.addWidget(QPushButton("Wireframe / Solid", clicked=self.toggle_wire))
        panel.addWidget(QPushButton("Perspective / Orthographic", clicked=self.toggle_proj))
        panel.addWidget(QPushButton("Reset", clicked=self.reset))

        panel.addStretch()
        return panel

    # ---------- Fonksiyonlar ----------
    def translate(self):
        self.gl.tx += self.tx.value()
        self.gl.ty += self.ty.value()
        self.gl.tz += self.tz.value()
        self.gl.update()

    def rotate(self):
        self.gl.angx += self.angx.value()
        self.gl.angy += self.angy.value()
        self.gl.angz += self.angz.value()
        self.gl.px = self.px.value()
        self.gl.py = self.py.value()
        self.gl.pz = self.pz.value()
        self.gl.use_arbitrary = self.arbitrary.isChecked()
        self.gl.update()

    def scale(self):
        if self.keep_ratio.isChecked():
            v = self.sx.value() / 100
            self.gl.sx += v
            self.gl.sy += v
            self.gl.sz += v
        else:
            self.gl.sx += self.sx.value() / 100
            self.gl.sy += self.sy.value() / 100
            self.gl.sz += self.sz.value() / 100
        self.gl.update()

    def mirror(self):
        if self.mx.isChecked(): self.gl.sx *= -1
        if self.my.isChecked(): self.gl.sy *= -1
        if self.mz.isChecked(): self.gl.sz *= -1
        self.gl.update()

    def shear(self):
        if self.shx.isChecked():
            self.gl.shear_matrix = [1,0.5,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
        elif self.shy.isChecked():
            self.gl.shear_matrix = [1,0,0,0, 0.5,1,0,0, 0,0,1,0, 0,0,0,1]
        elif self.shz.isChecked():
            self.gl.shear_matrix = [1,0,0,0, 0,1,0,0, 0.5,0,1,0, 0,0,0,1]
        self.gl.update()

    def toggle_wire(self):
        self.gl.wireframe = not self.gl.wireframe
        self.gl.update()

    def toggle_proj(self):
        self.gl.perspective = not self.gl.perspective
        self.gl.resizeGL(self.gl.width(), self.gl.height())
        self.gl.update()

    def reset(self):
        self.gl.reset_state()
        self.gl.update()


app = QApplication(sys.argv)
w = MainWindow()
w.resize(1200, 750)
w.show()
sys.exit(app.exec_())