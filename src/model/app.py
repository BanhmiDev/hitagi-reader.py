#!/usr/bin/env python
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QDir, Qt
from PyQt5.QtGui import QFont, QIcon, QImage, QClipboard
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QFileDialog, QMessageBox

from model.canvas import CanvasModel

class AppModel(object):

    def __init__(self):
        self.canvas = CanvasModel()

        self.clipboard = QApplication.clipboard()

        self.hide_menubar = True
        self.hide_statusbar = True

        self.is_fullscreen = False # fullscreen mode
        self.image_paths = [] # images of the current directory

        self._update_funcs = []

        # variable placeholders
        self.include_subfolders = True
        self.image_index = -1 # index of current shown image
        self.directory = None
        self.image = None

        self.scaleFactor = 1

    # subscribe a view method for updating
    def subscribe_update_func(self, func):
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    # unsubscribe a view method for updating
    def unsubscribe_update_func(self, func):
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    # update registered view methods
    def announce_update(self):
        for func in self._update_funcs:
            func()

    def get_image(self):
        return QImage(str(self.image_paths[self.image_index])) if self.image_index != -1 else None

    def get_image_path(self):
        return str(self.image_paths[self.image_index]) if self.image_index > -1 else None

    def change_directory(self, directory = None):
        if not directory:
            new_directory = QFileDialog.getExistingDirectory(None, "Change directory", '/')
        else:
            new_directory = directory

        # if canceled, return nothing
        if not new_directory:
            return

        # subfolder management
        if self.include_subfolders == True:
            _image_paths = [i for i in Path(new_directory).rglob("*") if i.suffix.lower() in ['.jpg', '.png']]
        else:
            _image_paths = [i for i in Path(new_directory).glob("*") if i.suffix.lower() in ['.jpg', '.png']]

        if len(_image_paths) > 0:
            self.image_paths = _image_paths
            self.image_index = 0
            self.directory = new_directory
            self.image = self.get_image()
        else:
            print("no images")
            