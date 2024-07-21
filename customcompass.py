from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import math

TILE_SIZE = 256
ZOOM_LEVEL = 15

PATH_TO_TILES = r"C:/Users/dprerad/Desktop/CompassQTPlugin/output/1721417545066";

DOT_RADIUS = 10

import logging
logging.basicConfig(
    filename='custom_compass.log', 
    level=logging.ERROR,           
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CustomCompass(QWidget):
    checkpointReached = Signal(int, float, float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lat = None
        self.lon = None

        self.xtile = None
        self.ytile = None

        self.dot_x = 0
        self.dot_y = 0

        self.pixmap = QPixmap()        
        self.adjacent_pixmaps = {}

        self.angleFromNorth = 0

        self.checkpoints = []

        self.setFixedSize(400, 300)

    def set_angle_from_north(self, angleFromNorth):
        self.angleFromNorth = angleFromNorth
        self.update()

    def update_coordinates(self, lat, lon):
        self.lat = lat
        self.lon = lon
        
        self.update_tile()
        
    def update_tile(self):
        new_xtile, new_ytile = self.lat_lon_to_tile_xy(self.lat, self.lon, ZOOM_LEVEL)
        if new_xtile != self.xtile or new_ytile != self.ytile:
            self.xtile, self.ytile = new_xtile, new_ytile
            self.load_adjacent_tiles()
        self.dot_x, self.dot_y = self.lat_lon_to_pixel(self.lat, self.lon, TILE_SIZE, ZOOM_LEVEL)
        self.dot_x %= TILE_SIZE
        self.dot_y %= TILE_SIZE
        
        self.update()

    def load_adjacent_tiles(self):
        """ Load the tile and its adjacent tiles. """
        self.adjacent_pixmaps.clear()
        
        adjacent_tiles = [
            (self.xtile - 2, self.ytile - 2), (self.xtile - 1, self.ytile - 2), (self.xtile, self.ytile - 2), (self.xtile + 1, self.ytile - 2), (self.xtile + 2, self.ytile - 2),
            (self.xtile - 2, self.ytile - 1), (self.xtile - 1, self.ytile - 1), (self.xtile, self.ytile - 1), (self.xtile + 1, self.ytile - 1), (self.xtile + 2, self.ytile - 1),
            (self.xtile - 2, self.ytile), (self.xtile - 1, self.ytile), (self.xtile, self.ytile), (self.xtile + 1, self.ytile), (self.xtile + 2, self.ytile),
            (self.xtile - 2, self.ytile + 1), (self.xtile - 1, self.ytile + 1), (self.xtile, self.ytile + 1), (self.xtile + 1, self.ytile + 1), (self.xtile + 2, self.ytile + 1),
            (self.xtile - 2, self.ytile + 2), (self.xtile - 1, self.ytile + 2), (self.xtile, self.ytile + 2), (self.xtile + 1, self.ytile + 2), (self.xtile + 2, self.ytile + 2)
        ]
        
        for x, y in adjacent_tiles:
            tile_path = f'{PATH_TO_TILES}/{ZOOM_LEVEL}/{x}/{y}.png'
            pixmap = QPixmap(tile_path)
            if not pixmap.isNull():
                self.adjacent_pixmaps[(x, y)] = pixmap

    def drawCompassNeedle(self, painter):
        painter.setPen(QPen(Qt.blue, 2))
        painter.setBrush(QBrush(Qt.blue))
        blue_triangle = QPolygon([
            QPoint(-5 + self.dot_x, self.dot_y),
            QPoint(5 + self.dot_x, self.dot_y),
            QPoint(self.dot_x, 30 + self.dot_y)
        ])
        painter.drawPolygon(blue_triangle)

        painter.setPen(QPen(Qt.red, 2))
        painter.setBrush(QBrush(Qt.red))
        red_triangle = QPolygon([
            QPoint(-5 + self.dot_x, self.dot_y),
            QPoint(5 + self.dot_x, self.dot_y),
            QPoint(self.dot_x, -30 + self.dot_y)
        ])
        painter.drawPolygon(red_triangle)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(self.dot_x - DOT_RADIUS, self.dot_y - DOT_RADIUS, DOT_RADIUS * 2, DOT_RADIUS * 2)

        painter.setFont(QFont('Arial', 20, QFont.Bold))
    
        painter.setPen(QPen(Qt.white)) 
        painter.drawText(QPoint(-10 + self.dot_x, -30 + self.dot_y - 10), 'N')
        painter.drawText(QPoint(-9 + self.dot_x, -30 + self.dot_y - 10), 'N')
        painter.drawText(QPoint(-11 + self.dot_x, -30 + self.dot_y - 10), 'N')
        painter.drawText(QPoint(-10 + self.dot_x, -30 + self.dot_y - 11), 'N')
        painter.drawText(QPoint(-10 + self.dot_x, -30 + self.dot_y - 9), 'N')

        painter.setPen(QPen(Qt.white))
        painter.drawText(QPoint(-10 + self.dot_x, 30 + self.dot_y + 25), 'S')
        painter.drawText(QPoint(-9 + self.dot_x, 30 + self.dot_y + 25), 'S')
        painter.drawText(QPoint(-11 + self.dot_x, 30 + self.dot_y + 25), 'S')
        painter.drawText(QPoint(-10 + self.dot_x, 30 + self.dot_y + 26), 'S')
        painter.drawText(QPoint(-10 + self.dot_x, 30 + self.dot_y + 24), 'S')

        painter.setPen(QPen(Qt.black))
        painter.drawText(QPoint(-10 + self.dot_x, -30 + self.dot_y - 10), 'N')
        painter.drawText(QPoint(-10 + self.dot_x, 30 + self.dot_y + 25), 'S')


    def paintEvent(self, event):
        painter = QPainter(self)

        if self.adjacent_pixmaps:
            offset_x = self.width() / 2 - self.dot_x
            offset_y = self.height() / 2 - self.dot_y
            
            painter.translate(offset_x, offset_y)
            
            painter.translate(self.dot_x, self.dot_y)
            painter.rotate(self.angleFromNorth)
            painter.translate(-self.dot_x, -self.dot_y)
            
            for (x, y), pixmap in self.adjacent_pixmaps.items():
                if not pixmap.isNull():
                    # Draw the pixmap with blending
                    painter.drawPixmap((x - self.xtile) * TILE_SIZE, (y - self.ytile) * TILE_SIZE, pixmap)
            
            self.drawCompassNeedle(painter)

            for (checkpoint_id, lon, lat, traversed) in self.checkpoints:
                pixel_x, pixel_y = self.lat_lon_to_pixel(lat, lon, TILE_SIZE, ZOOM_LEVEL)
                pixel_x %= TILE_SIZE
                pixel_y %= TILE_SIZE

                painter.setPen(QPen(Qt.black, 2))
                painter.setBrush(QBrush(Qt.green if traversed else Qt.blue))
                painter.drawEllipse(pixel_x - 5, pixel_y - 5, 10, 10)

            painter.resetTransform()
            
    def lat_lon_to_tile_xy(self, lat, lon, zoom):
        n = 2.0 ** zoom
        xtile = (lon + 180.0) / 360.0 * n
        ytile = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
        return int(xtile), int(ytile)

    def lat_lon_to_pixel(self, lat, lon, tile_size, zoom):
        xtile, ytile = self.lat_lon_to_tile_xy(lat, lon, zoom)
        pixel_x = (lon + 180.0) / 360.0 * (2 ** zoom * tile_size) % tile_size
        pixel_y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * (2 ** zoom * tile_size) % tile_size
        return pixel_x, pixel_y

    def minimumSizeHint(self):
        return QSize(150, 150)

    def sizeHint(self):
        return QSize(150, 150)
    
    def add_checkpoint(self, checkpoint_id, longitude, latitude):
        """ Add a checkpoint to the list. """
        self.checkpoints.append((checkpoint_id, longitude, latitude, False))

    def remove_checkpoint_by_id(self, checkpoint_id):
        """ Remove a checkpoint from the list by its ID. """
        self.checkpoints = [cp for cp in self.checkpoints if cp[0] != checkpoint_id]

    def check_vicinity(self, current_longitude, current_latitude, vicinity_threshold):
        """ Check if the current coordinates are within the vicinity of any checkpoint and mark it as traversed. """
        for i, (checkpoint_id, lon, lat, traversed) in enumerate(self.checkpoints):
            if not traversed and self.is_in_vicinity(current_longitude, current_latitude, lon, lat, vicinity_threshold):
                self.checkpoints[i] = (checkpoint_id, lon, lat, True)
                self.checkpointReached.emit(self.checkpointReached.emit(checkpoint_id, lon, lat))
                return (checkpoint_id, lon, lat, True)
        return None

    @staticmethod
    def is_in_vicinity(current_longitude, current_latitude, checkpoint_lon, checkpoint_lat, threshold):
        """ Helper method to determine if current coordinates are within the threshold distance from a checkpoint. """
        distance = ((current_longitude - checkpoint_lon) ** 2 + (current_latitude - checkpoint_lat) ** 2) ** 0.5
        return distance <= threshold

    @Property(str)
    def longitude(self):
        return str(self.lon)
    
    @longitude.setter
    def longitude(self, lon_str):
        try:
            self.lon = float(lon_str)
        except ValueError as e:
            print(f"Not a floating point number: {lon_str}")
            logging.error(f"Failed to convert longitude '{lon_str}' to float: {e}")
    
    @Property(str)
    def latitude(self):
        return str(self.lat)
    
    @latitude.setter
    def latitude(self, lat_str):
        try:
            self.lat = float(lat_str)
        except ValueError as e:
            print(f"Not a floating point number: {lat_str}")
            logging.error(f"Failed to convert latitude '{lat_str}' to float: {e}")


################# Testing ###################

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    compass = CustomCompass()

    compass.setWindowTitle("Custom compass plugin test")

    center_lat = 44.795059201407355
    center_lon = 17.205532194807446
    compass.update_coordinates(center_lat, center_lon)

    compass.add_checkpoint(1, 17.205232195807446, 44.785069201407355)
    compass.add_checkpoint(2, 17.210000000000000, 44.800000000000000)

    angle = 0
    def update_angle():
        global angle
        angle = (angle + 1) % 360
        compass.set_angle_from_north(angle)
    
    timer = QTimer()
    timer.timeout.connect(update_angle)
    timer.start(50)

    compass.show()
    sys.exit(app.exec())

################# Testing ###################