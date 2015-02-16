#!/usr/bin/env python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

class CanvasModel(object):

    def __init__(self):
        self.scene = QGraphicsScene() # Canvas area
        self.scale_factor = 1 # Scaling factor
        self.current_image = None # Current image in canvas

    def update(self):
        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(QPixmap.fromImage(self.current_image)))
        self.scene.update()
            