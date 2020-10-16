from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import QPoint
from math import sqrt
import numpy as np
import sys


class Canvas(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.flag = 1

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.canv = QPixmap()

        self.button_1 = QPushButton("DDA")
        self.button_1.setEnabled(False)
        self.button_1.clicked.connect(self.btn_1)

        self.button_2 = QPushButton("Bresenham's Line")
        self.button_2.setEnabled(True)
        self.button_2.clicked.connect(self.btn_2)

        self.button_3 = QPushButton("Bresenham's Circle")
        self.button_3.setEnabled(True)
        self.button_3.clicked.connect(self.btn_3)

        self.button_4 = QPushButton("Bazier")
        self.button_4.setEnabled(True)
        self.button_4.clicked.connect(self.btn_4)

        self.placeholder = QWidget()
        self.grid.addWidget(self.button_1, 0, 0, 2, 10)
        self.grid.addWidget(self.button_2, 0, 10, 2, 10)
        self.grid.addWidget(self.button_3, 0, 20, 2, 10)
        self.grid.addWidget(self.button_4, 0, 30, 2, 10)
        self.grid.addWidget(self.placeholder, 1, 0, 50, 40)

        self.chosen_points = []
        self.start = None
        self.end = None
        self.opor = None
        self.resize(640, 480)
        self.show()

    def btn_1(self):
        self.flag = 1
        self.button_1.setEnabled(False)
        self.button_2.setEnabled(True)
        self.button_3.setEnabled(True)
        self.button_4.setEnabled(True)
        self.chosen_points = []

    def btn_2(self):
        self.flag = 2
        self.button_1.setEnabled(True)
        self.button_2.setEnabled(False)
        self.button_3.setEnabled(True)
        self.button_4.setEnabled(True)
        self.chosen_points = []
        for pos in self.chosen_points:
            painter.drawPoint(pos)

    def btn_3(self):
        self.flag = 3
        self.button_1.setEnabled(True)
        self.button_2.setEnabled(True)
        self.button_3.setEnabled(False)
        self.button_4.setEnabled(True)
        self.chosen_points = []

    def btn_4(self):
        self.flag = 4
        self.button_1.setEnabled(True)
        self.button_2.setEnabled(True)
        self.button_3.setEnabled(True)
        self.button_4.setEnabled(False)
        self.chosen_points = []

    def paintEvent(self, paint_event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.canv)
        
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        for pos in self.chosen_points:
            painter.drawPoint(pos)

    def mouseReleaseEvent(self, cursor_event):
        if self.start == None:
            self.start = [cursor_event.x(), cursor_event.y()]
        elif self.end == None:
            self.end = [cursor_event.x(), cursor_event.y()]
            if self.flag == 1:
                self.dda()
                self.start = None
                self.end = None
            elif self.flag == 2:
                self.bresenhams_line()
                self.start = None
                self.end = None
            elif self.flag == 3:
                self.bresenhams_circle()
                self.start = None
                self.end = None
        else:
            self.opor = [cursor_event.x(), cursor_event.y()]
            if self.flag == 4:
                self.bazier()
                self.start = None
                self.end = None
                self.opor = None
        self.chosen_points.append(cursor_event.pos())
        self.update()

    def dda(self):
        def sign(x):
            if x > 0:
                return 1
            elif x < 0:
                return -1
            elif x == 0:
                return 0

        if abs(self.end[0] - self.start[0]) >= abs(self.end[1] - self.start[1]):
            lengh = abs(self.end[0] - self.start[0])
        else:
            lengh = abs(self.end[1] - self.start[1])
        Dx = (self.end[0] - self.start[0]) / lengh
        Dy = (self.end[1] - self.start[1]) / lengh
        x = self.start[0] + 0.5 * sign(Dx)
        y = self.start[1] + 0.5 * sign(Dy)
        i = 1
        while i <= lengh:
            self.chosen_points.append(QPoint(x, y))
            x = x + Dx
            y = y + Dy
            i += 1

    def bresenhams_line(self):
        x_err = 0
        y_err = 0
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        incX = 0
        incY = 0
        if dx > 0:
            incX = 1
        elif dx != 0:
            incX = -1

        if dy > 0:
            incY = 1
        elif dy != 0:
            incY = -1

        dx = abs(dx)
        dy = abs(dy)
        d = max(dx, dy)

        x = self.start[0]
        y = self.start[1]
        for i in range(d):
            x_err += dx
            y_err += dy
            if x_err >= d:
                x += incX
                x_err -= d
            if y_err >= d:
                y += incY
                y_err -= d
            self.chosen_points.append(QPoint(x, y))

    def bresenhams_circle(self):
        r = sqrt((self.end[0] - self.start[0])**2 + (self.end[1] - self.start[1])**2) 
        x = 0
        y = r
        delta = 1 - 2 * r
        error = 0
        while y >= 0:
            self.chosen_points.append(QPoint(self.start[0] + x, self.start[1] + y))
            self.chosen_points.append(QPoint(self.start[0] + x, self.start[1] - y))
            self.chosen_points.append(QPoint(self.start[0] - x, self.start[1] + y))
            self.chosen_points.append(QPoint(self.start[0] - x, self.start[1] - y))
            error = 2 * (delta + y) - 1
            if (delta < 0 and error <= 0):
                x += 1
                delta = delta + (2 * x + 1)
                continue
            error = 2 * (delta - x) - 1
            if (delta > 0 and error > 0):
                y -= 1
                delta = delta + (1 - 2 * y)
                continue
            x += 1
            delta = delta + 2 * (x - y)
            y -= 1

    def bazier(self):
        one = np.array(self.start)
        two = np.array(self.end)
        three = np.array(self.opor)

        def f(p1, p2, p3):
            t = np.linspace(0, 1, 1000)
            for i in t:
                ans = ((1-i)**2) * p1 + 2*(1-i)*i*p2 + (i**2)*p3
                x, y = ans[0], ans[1]
                self.chosen_points.append(QPoint(x, y))

        f(one, three, two)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Canvas()
    sys.exit(app.exec_())
