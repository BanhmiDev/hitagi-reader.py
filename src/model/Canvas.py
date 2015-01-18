#!/usr/bin/env python
from pathlib import Path

from PyQt5.QtCore import (pyqtSlot, QDir, Qt)
from PyQt5.QtGui import (QFont, QIcon, QImage)

from model import Model

class Canvas(object):

    def __init__(self, main_model):
        self.model = main_model

    # Update on resize etc.
    def update_canvas(self, container_width, container_height):
        image = self.model.get_image()

        if image != None:
            #self.setWindowTitle("Hitagi - " + str(self.image_paths[self.image_index]) + "    " + str(self.image_index + 1) + " of " + str(len(self.image_paths)))
            container_size = (container_width, container_height)
            image_size = (image.width(), image.height())
            ratio = [image_size[0] / container_size[0], image_size[1] / container_size[1]]
            if ratio[0] > 1 and ratio[0] > ratio[1]:
                image = image.scaledToWidth(container_size[0], Qt.SmoothTransformation)
            elif ratio[1] > 1 and ratio[1] > ratio[0]:
                image = image.scaledToHeight(container_size[1], Qt.SmoothTransformation)

            self.model.image = image

    # Toggle fullscreen mode
    def toggle_fullscreen(self):
        # if already in fullscreen mode
        if self.model.is_fullscreen:
            self.model.is_fullscreen = False
        else:
            self.model.is_fullscreen = True