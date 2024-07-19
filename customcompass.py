from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import os

class CustomCompass(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "WorldMap.png")
        self.background_image = QPixmap(image_path)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.white)
        self.setPalette(palette)

        self.setFixedSize(400, 300)
        self.angle = 0

    def set_angle(self, angle):
        self.angle = angle
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        widget_width = self.width()
        widget_height = self.height()
        
        size = min(widget_width, widget_height)
        
        top_left_x = (widget_width - size) // 2
        top_left_y = (widget_height - size) // 2
        
        square_rect = QRect(top_left_x, top_left_y, size, size)
        
        painter.drawPixmap(square_rect, self.background_image.scaled(size, size, Qt.KeepAspectRatioByExpanding))

        center_x = self.width() // 2
        center_y = self.height() // 2

        painter.translate(center_x, center_y)
        painter.rotate(self.angle)

        needle_length = size // 3

        painter.setPen(QPen(Qt.red, 2))
        painter.setBrush(QBrush(Qt.red))
        red_triangle = QPolygon([
            QPoint(-5, 0),
            QPoint(5, 0),
            QPoint(0, -needle_length)
        ])
        painter.drawPolygon(red_triangle)

        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(QBrush(Qt.blue))
        blue_triangle = QPolygon([
            QPoint(-5, 0),
            QPoint(5, 0),
            QPoint(0, needle_length)
        ])
        painter.drawPolygon(blue_triangle)

        painter.setFont(QFont('Arial', 20, QFont.Bold))
        
        painter.setPen(QPen(Qt.white)) 
        painter.drawText(QPoint(-10, -needle_length - 10), 'N')
        painter.drawText(QPoint(-9, -needle_length - 10), 'N')
        painter.drawText(QPoint(-11, -needle_length - 10), 'N')
        painter.drawText(QPoint(-10, -needle_length - 11), 'N')
        painter.drawText(QPoint(-10, -needle_length - 9), 'N')

        painter.setPen(QPen(Qt.white))
        painter.drawText(QPoint(-10, needle_length + 25), 'S')
        painter.drawText(QPoint(-9, needle_length + 25), 'S')
        painter.drawText(QPoint(-11, needle_length + 25), 'S')
        painter.drawText(QPoint(-10, needle_length + 26), 'S')
        painter.drawText(QPoint(-10, needle_length + 24), 'S')

        painter.setPen(QPen(Qt.black))
        painter.drawText(QPoint(-10, -needle_length - 10), 'N')
        painter.drawText(QPoint(-10, needle_length + 25), 'S')

        painter.resetTransform()

    def minimumSizeHint(self):
        return QSize(150, 150)

    def sizeHint(self):
        return QSize(150, 150)

################# Testing ###################

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = CustomCompass()
    
    def update_angle():
        new_angle = (window.angle + 1) % 360
        window.set_angle(new_angle)
    
    timer = QTimer()
    timer.timeout.connect(update_angle)
    timer.start(10)

    window.show()
    sys.exit(app.exec())

################# Testing ###################