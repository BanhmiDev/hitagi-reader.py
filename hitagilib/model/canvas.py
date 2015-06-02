#!/usr/bin/env python3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

class CanvasModel(object):

    def __init__(self):
        self.scene = QGraphicsScene() # Canvas area
        self.scale_factor = 1 # Scaling factor
        self.o_image = None # Original image, used for scaling
        self.image = None # Image viewable in our canvas
        self.c_width = 0 # Container width
        self.c_height = 0 # Container height

    def setImage(self, image):
        self.o_image = image

    def setGeometry(self, container_width, container_height):
        self.c_width = container_width
        self.c_height = container_height

    def update_image(self, selection):
        if self.o_image is not None:
            # Selection defines the viewport behaviour
            # 0: Ratio scaling (uses canvas/image-size)
            # 1: Scale to container width
            # 2: Scale to container height
            # 3: Scale to original size
            if selection == 0:
                ratio = [self.o_image.width() / self.c_width, self.o_image.height() / self.c_height]
                if ratio[0] > 1 and ratio[0] > ratio[1]:
                    self.image = self.o_image.scaledToWidth(self.c_width, Qt.SmoothTransformation)
                elif ratio[1] > 1 and ratio[1] > ratio[0]:
                    self.image = self.o_image.scaledToHeight(self.c_height, Qt.SmoothTransformation)
            elif selection == 1:
                self.image = self.o_image.scaledToWidth(self.c_width, Qt.SmoothTransformation)
            elif selection == 2:
                self.image = self.o_image.scaledToHeight(self.c_height, Qt.SmoothTransformation)
            elif selection == 3:
                self.image = self.o_image

            # Centering and dragging 'fix'
            if self.image.width() < self.c_width:
                delta_x = self.c_width - self.image.width()
            else:
                delta_x = 0

            full_container_width = self.image.width() + delta_x * 2
            self.scene.setSceneRect(-delta_x, 0, full_container_width, self.image.height())
 
            # Update scene
            self.scene.clear()
            self.scene.addItem(QGraphicsPixmapItem(QPixmap.fromImage(self.image)))
            self.scene.update()

    def scale_image(self, factor):
        if self.o_image is not None:
            self.scale_factor *= factor
            self.image = self.o_image.scaled(self.image.width() * self.scale_factor, self.image.height() * self.scale_factor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Reset scale factor
            self.scale_factor = 1

            # Centering and dragging 'fix'
            if self.image.width() < self.c_width:
                delta_x = self.c_width - self.image.width()
            else:
                delta_x = 0

            full_container_width = self.image.width() + delta_x * 2
            self.scene.setSceneRect(-delta_x, 0, full_container_width, self.image.height())
 
            self.scene.clear()
            self.scene.addItem(QGraphicsPixmapItem(QPixmap.fromImage(self.image)))
            self.scene.update()

    def rotate_image(self):
        if self.image is not None:
            # Rotate the original and viewable image to ensure a constant workflow when modifying from canvas
            matrix = QTransform()
            matrix.translate(self.image.width() / 2, self.image.height() / 2)
            matrix.rotate(90)
            matrix.translate(-self.image.width() / 2, -self.image.height() / 2)
            
            # Save transformed image
            self.image = self.image.transformed(matrix)
           
            o_matrix = QTransform()
            o_matrix.translate(self.o_image.width() / 2, self.o_image.height() / 2)
            o_matrix.rotate(90)
            o_matrix.translate(-self.o_image.width() / 2, -self.o_image.height() / 2)
            
            # Save transformed image
            self.o_image = self.o_image.transformed(o_matrix)

            self.scene.clear()
            self.scene.addItem(QGraphicsPixmapItem(QPixmap.fromImage(self.image)))
            self.scene.setSceneRect(-self.c_width / 2, 0, self.c_width * 2, self.c_height)
            self.scene.update()

    def flip_image(self, direction):
        if self.image is not None:
            if direction == 0:
                self.image = self.image.mirrored(True, False)
                self.o_image = self.o_image.mirrored(True, False)
            else:
                self.image = self.image.mirrored(False, True)
                self.o_image = self.o_image.mirrored(False, True)

            self.scene.clear()
            self.scene.addItem(QGraphicsPixmapItem(QPixmap.fromImage(self.image)))
            self.scene.update()    
