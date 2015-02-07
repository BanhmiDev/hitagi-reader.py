#!/usr/bin/env python
from PyQt5 import uic
from PyQt5.QtCore import (pyqtSlot, QDir)
from PyQt5.QtGui import (QFont, QIcon, QImage)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileSystemModel)

from controller.canvas import CanvasController
#from controller.settings import SettingsController

class MainController(object):

    def __init__(self, model):
        self.model = model
        self.canvas = CanvasController(self.model.canvas)

    # called from view class
    def change_include_subfolders(self, checked):
        # put control logic here
        self.model.include_subfolders = checked
        self.model.announce_update()

    def change_directory(self, container_width, container_height, directory = None):
        self.model.change_directory(directory)
        image = self.model.get_image()
        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    def update_canvas(self, container_width, container_height, image = None):
        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    def toggle_fullscreen(self):
        self.model.toggle_fullscreen()
        self.model.announce_update()

    def prev_image(self, container_width, container_height):
        self.model.prev_image()
        image = self.model.get_image()
        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    def next_image(self, container_width, container_height):
        self.model.next_image()
        image = self.model.get_image()
        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    def set_wallpaper(self):
        self.model.set_wallpaper()
        