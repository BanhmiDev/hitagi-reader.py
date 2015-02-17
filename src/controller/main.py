#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QDir, QThread
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog

from model.settings import SettingsModel
from model.favorites import FavoritesModel
from controller.canvas import CanvasController

class MainController(object):

    def __init__(self, model):
        self.settings = SettingsModel()
        self.favorites = FavoritesModel()
        self.model = model
        self.canvas = CanvasController(self.model.canvas)

    def change_directory(self, directory = None):
        """Change current directory."""
        if not directory:
            new_directory = QFileDialog.getExistingDirectory(None, "Change directory", '/')
        else:
            new_directory = directory

        # if canceled, return nothing
        if not new_directory:
            return

        # old concept: open directory and load paths of images
        #if self.model.include_subfolders == True:
        #    _image_paths = [i for i in Path(new_directory).rglob("*") if i.suffix.lower() in ['.jpg', '.png']]
        #else:
        #    _image_paths = [i for i in Path(new_directory).glob("*") if i.suffix.lower() in ['.jpg', '.png']]

        #if len(_image_paths) > 0:
            #self.model.image_paths = _image_paths
            #self.model.image_index = 0

        self.model.directory = new_directory
        #print(Path(str(new_directory)))

        #image = self.model.get_image()
        #self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    def add_to_favorites(self):
        """Favorite current directory."""
        self.favorites.add(str(self.model.directory))
        self.favorites.save()

    def remove_from_favorites(self):
        """Remove current directory from favorite list."""
        self.favorites.remove(str(self.model.directory))
        self.favorites.save()

    def update_canvas(self, container_width, container_height, image = None):
        """Update canvas with image."""
        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    def toggle_fullscreen(self):
        """Toggle between fullscreen mode."""
        if self.model.is_fullscreen:
            self.model.is_fullscreen = False
        else:
            self.model.is_fullscreen = True

        # Update UI
        self.model.announce_update()

    def open_image(self, container_width, container_height, path):
        """Open specific image via path."""
        image = QImage(str(path))
        self.model.image_path = path
        # Update image index
        #if _path in self.model.image_paths:
            #self.model.image_index = self.model.image_paths.index(_path)

        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    #def prev_image(self, container_width, container_height):
    #    """Go to previous image."""
    #    if self.model.image_index > 0:
    #        self.model.image_index -= 1
    #    image = self.model.get_image()
    #
    #    # Use canvas controller
    #    self.canvas.update_canvas(container_width, container_height, image)
    #    self.model.announce_update()
    #
    #def next_image(self, container_width, container_height):
    #    """Go to next image."""
    #    if self.model.image_index < (len(self.model.image_paths) - 1):
    #        self.model.image_index += 1
    #    image = self.model.get_image()
    #
    #    self.canvas.update_canvas(container_width, container_height, image)
    #    self.model.announce_update()

    def copy_to_clipboard(self):
        if self.model.image_path is not None:
            self.model.clipboard.setImage(self.get_image(), QClipboard.Clipboard)
        