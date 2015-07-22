#!/usr/bin/env python3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QGraphicsScene

from hitagilib.widget.CustomQGraphicsPixmapItem import CustomQGraphicsPixmapItem
        
class CanvasModel(object):
    def __init__(self):
        self.scene = QGraphicsScene() # Canvas area
        self.scale_factor = 1 # Scaling factor
        self.original_image = None # Original image, used for scaling
        self.image = None # Image viewable in our canvas
        self.c_width = 0 # Container width
        self.c_height = 0 # Container height
        
    def set_image(self, image):
        self.original_image = image

    def setGeometry(self, container_width, container_height):
        self.c_width = container_width
        self.c_height = container_height
        self.scene.setSceneRect(0, 0, self.c_width, self.c_height)

    def update_image(self, selection):
        # Check for container width to prevent behaviour when container is not initialized yet (ex. passing an image as argument)
        if self.original_image is not None and self.c_width != 0:
            # Selection defines the viewport behaviour
            # 0: Ratio scaling (uses canvas/image-size)
            # 1: Scale to container width
            # 2: Scale to container height
            # 3: Scale to original size
            if selection == 0:
                ratio = [self.original_image.width() / self.c_width, self.original_image.height() / self.c_height]
                if ratio[0] > 1 and ratio[0] > ratio[1]:
                    self.image = self.original_image.scaledToWidth(self.c_width, Qt.SmoothTransformation)
                elif ratio[1] > 1 and ratio[1] > ratio[0]:
                    self.image = self.original_image.scaledToHeight(self.c_height, Qt.SmoothTransformation)
                else: # Small image, show in original size
                    self.image = self.original_image
            elif selection == 1:
                self.image = self.original_image.scaledToWidth(self.c_width, Qt.SmoothTransformation)
            elif selection == 2:
                self.image = self.original_image.scaledToHeight(self.c_height, Qt.SmoothTransformation)
            elif selection == 3:
                self.image = self.original_image

            # Update scene
            self.scene.clear()
            self.scene.addItem(CustomQGraphicsPixmapItem(QPixmap.fromImage(self.image), self.c_width, self.c_height))
            self.scene.update()

    def scale_image(self, factor):
        if self.original_image is not None:
            self.scale_factor *= factor
            self.image = self.original_image.scaled(self.image.width() * self.scale_factor, self.image.height() * self.scale_factor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Reset scale factor
            self.scale_factor = 1
 
            self.scene.clear()
            self.scene.addItem(CustomQGraphicsPixmapItem(QPixmap.fromImage(self.image), self.c_width, self.c_height))
            self.scene.update()

    def rotate_image(self, rotation):
        if self.original_image is not None:
            print(rotation)
            # Rotate the original and viewable image to ensure a constant workflow when modifying from canvas
            matrix = QTransform()
            matrix.translate(self.image.width() / 2, self.image.height() / 2)
            matrix.rotate(rotation)
            matrix.translate(-self.image.width() / 2, -self.image.height() / 2)
            
            # Save transformed image
            self.image = self.image.transformed(matrix)
           
            original_matrix = QTransform()
            original_matrix.translate(self.original_image.width() / 2, self.original_image.height() / 2)
            original_matrix.rotate(rotation)
            original_matrix.translate(-self.original_image.width() / 2, -self.original_image.height() / 2)
            
            # Save transformed image
            self.original_image = self.original_image.transformed(original_matrix)

            self.scene.clear()
            self.scene.addItem(CustomQGraphicsPixmapItem(QPixmap.fromImage(self.image), self.c_width, self.c_height))
            self.scene.update()

    def flip_image(self, direction):
        if self.original_image is not None:
            if direction == 0:
                self.image = self.image.mirrored(True, False)
                self.original_image = self.original_image.mirrored(True, False)
            else:
                self.image = self.image.mirrored(False, True)
                self.original_image = self.original_image.mirrored(False, True)

            self.scene.clear()
            self.scene.addItem(CustomQGraphicsPixmapItem(QPixmap.fromImage(self.image), self.c_width, self.c_height))
            self.scene.update()    
