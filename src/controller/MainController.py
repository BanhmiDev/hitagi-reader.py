#!/usr/bin/env python
from PyQt5 import uic
from PyQt5.QtCore import (pyqtSlot, QDir)
from PyQt5.QtGui import (QFont, QIcon, QImage)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileSystemModel)

from model import Canvas

class MainController(object):

    def __init__(self, model):
        self.model = model
        self.canvas = Canvas.Canvas(model)

    # called from view class
    def change_include_subfolders(self, checked):
        # put control logic here
        self.model.include_subfolders = checked
        self.model.announce_update()

    def change_directory(self, container_width, container_height):
        self.model.change_directory()
        self.canvas.update_canvas(container_width, container_height)
        self.model.announce_update()

    def update_canvas(self, container_width, container_height):
        self.canvas.update_canvas(container_width, container_height)
        self.model.announce_update()

    def toggle_fullscreen(self):
        self.canvas.toggle_fullscreen()
        self.model.announce_update()

    def prevImage(self):
        self.model.prevImage()

    def nextImage(self):
        self.model.nextImage()
