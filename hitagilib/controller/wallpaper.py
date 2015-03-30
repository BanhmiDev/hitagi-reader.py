#!/usr/bin/env python
from PyQt5.QtCore import QStandardPaths

import os

class WallpaperController(object):

    def __init__(self, model):
        self.model = model

    def set_as_wallpaper(self, option):
        """Set current image as wallpaper."""
        if self.model.image_path is not None:
            path = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
            self.model.get_image().save(path + "/test.bmp")
            subprocess.call(('feh', '--bg-fill', selectedImage))

        """windows
        import win32api, win32con, win32gui

        if self.model.get_image_path() is not None:
            tiled = "1" if option == 1 else "0"
            t =QStandardPaths.writableLocation(QStandardPaths.TempLocation)
            path = t
            print(self.model.get_image())
            # paths immer mit /
            print(self.model.get_image().save(path + "/test.bmp"))
            print(QStandardPaths.writableLocation(QStandardPaths.TempLocation))

            #key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
            #win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
            #win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, tiled)
            #win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)
        """