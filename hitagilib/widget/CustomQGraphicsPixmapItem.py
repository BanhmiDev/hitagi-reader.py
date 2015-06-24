#!/usr/bin/env python3
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

class CustomQGraphicsPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, c_width, c_height):
        QGraphicsPixmapItem.__init__(self, None)
        self.c_width = c_width # Container width
        self.c_height = c_height # Container height
        self.setPixmap(pixmap) # The pixmap
        self.setFlag(QGraphicsItem.ItemIsMovable) # Make it movable
        self.pixmap = self.pixmap() # just call it once

    def mouseMoveEvent(self, e):
        # Prevent item from going outside the scene
        # Hardcoded mess
        # TODO: replace with better solution
        super().mouseMoveEvent(e)

        pos_x = self.pos().x()
        pos_y = self.pos().y()

        self.image_width = self.pixmap.width()
        self.image_height = self.pixmap.height()

        delta_x = abs(self.c_width - self.image_width)
        delta_y = abs(self.c_height - self.image_height)

        # Prevent strange behaviours for images smaller than our container
        if self.image_width <= self.c_width and self.image_height <= self.c_height:
            if pos_x < 0:
                if pos_y < 0:
                    self.setPos(0, 0)
                else:
                    self.setPos(0, pos_y)
            elif pos_y < 0:
                if pos_x < 0:
                    self.setPos(0, 0)
                elif pos_x + self.image_width > self.c_width:
                    self.setPos(delta_x, 0)
                else:
                    self.setPos(pos_x, 0)

            if pos_x + self.image_width > self.c_width:
                if pos_y < 0:
                    self.setPos(delta_x, 0)
                elif pos_y + self.image_height > self.c_height:
                    self.setPos(delta_x, delta_y)
                else:
                    self.setPos(delta_x, pos_y)
            elif pos_y + self.image_height > self.c_height :
                if pos_x < 0:
                    self.setPos(0, delta_y)
                else:
                    self.setPos(pos_x, delta_y)
        elif self.image_width > self.c_width and self.image_height <= self.c_height: # Image width bigger than container
            if pos_x < -delta_x:
                if pos_y < 0:
                    self.setPos(-delta_x, 0)
                else:
                    self.setPos(-delta_x, pos_y)
            elif pos_y < 0:
                if pos_x < -delta_x:
                    self.setPos(-delta_x, 0)
                elif pos_x + self.image_width > self.c_width + delta_x:
                    self.setPos(0, 0)
                else:
                    self.setPos(pos_x, 0)

            if pos_x + self.image_width > self.c_width + delta_x:
                if pos_y < 0:
                    self.setPos(0, 0)
                elif pos_y + self.image_height > self.c_height:
                    self.setPos(0, delta_y)
                else:
                    self.setPos(0, pos_y)
            elif pos_y + self.image_height > self.c_height :
                if pos_x < -delta_x:
                    self.setPos(-delta_x, delta_y)
                else:
                    self.setPos(pos_x, delta_y)
        elif self.image_height > self.c_height and self.image_width <= self.c_width: # Image height bigger than container
            if pos_x < 0:
                if pos_y < -delta_y:
                    self.setPos(0, -delta_y)
                else:
                    self.setPos(0, pos_y)
            elif pos_y < -delta_y:
                if pos_x < 0:
                    self.setPos(0, 0)
                elif pos_x + self.image_width > self.c_width:
                    self.setPos(delta_x, 0)
                else:
                    self.setPos(pos_x, -delta_y)

            if pos_x + self.image_width > self.c_width:
                if pos_y < -delta_y:
                    self.setPos(delta_x, -delta_y)
                elif pos_y + self.image_height > self.c_height + delta_y:
                    self.setPos(delta_x, 0)
                else:
                    self.setPos(delta_x, pos_y)
            elif pos_y + self.image_height > self.c_height + delta_y:
                if pos_x < 0:
                    self.setPos(0, 0)
                else:
                    self.setPos(pos_x, 0)
        elif self.image_height > self.c_height and self.image_width > self.c_width: # Image width and height bigger than container
            if pos_x < -delta_x:
                if pos_y < -delta_y:
                    self.setPos(-delta_x, -delta_y)
                else:
                    self.setPos(-delta_x, pos_y)
            elif pos_y < -delta_y:
                if pos_x < -delta_x:
                    self.setPos(-delta_x, 0)
                elif pos_x + self.image_width > self.c_width + delta_x:
                    self.setPos(0, 0)
                else:
                    self.setPos(pos_x, -delta_y)

            if pos_x + self.image_width > self.c_width + delta_x:
                if pos_y < -delta_y:
                    self.setPos(0, -delta_y)
                elif pos_y + self.image_height > self.c_height + delta_y:
                    self.setPos(0, 0)
                else:
                    self.setPos(0, pos_y)
            elif pos_y + self.image_height > self.c_height + delta_y:
                if pos_x < -delta_x:
                    self.setPos(-delta_x, 0)
                else:
                    self.setPos(pos_x, 0)
