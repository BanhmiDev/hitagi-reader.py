#!/usr/bin/env python
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import (pyqtSlot, QDir, Qt)
from PyQt5.QtGui import (QFont, QIcon, QImage, QClipboard)
from PyQt5.QtWidgets import (QApplication, QFileSystemModel, QFileDialog, QMessageBox)

from model.canvas import CanvasModel

class AppModel(object):

    def __init__(self):
        self.canvas = CanvasModel()

        self.clipboard = QApplication.clipboard()

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
            new_directory = QFileDialog.getExistingDirectory(None, "HALLO", '/')
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

    def prev_image(self):
        if self.image_index != 0:
            self.image_index -= 1

    def next_image(self):
        if self.image_index < (len(self.image_paths) - 1):
            self.image_index += 1

    def toggle_fullscreen(self):
        # Already in fullscreen mode
        if self.is_fullscreen:
            self.is_fullscreen = False
        else:
            self.is_fullscreen = True

    def copy_to_clipboard(self):
        if self.image_index != -1:
            self.clipboard.setImage(self.get_image(), QClipboard.Clipboard)

    def set_wallpaper(self):
        import win32api, win32con, win32gui

        if self.get_image_path() is not None:
            path = self.get_image_path()

            key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
            win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
            win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
            win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)
