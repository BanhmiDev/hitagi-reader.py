#!/usr/bin/env python
import os
from subprocess import call, PIPE

from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QDesktopWidget

class WallpaperController(object):

    def __init__(self, model):
        self.model = model

    def set_as_wallpaper(self, option):
        """Set current image as wallpaper."""

        # TODO: mac version, testing

        path = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
        image = self.model.get_image()
        desktop_geometry = QDesktopWidget().screenGeometry()

        # Scale image according to option
        if option == 2:
            # Fit to desktop width
            image = image.scaledToWidth(desktop_geometry.width(), Qt.SmoothTransformation)
        elif option == 3:
            # Fit to desktop height
            image = image.scaledToHeight(desktop_geometry.height(), Qt.SmoothTransformation)

        image.save(path + "/hr_wallpaper.bmp") # Save new image
                
        if os.name == 'nt': # Windows
            import win32api, win32con, win32gui

            if self.model.get_image_path() is not None:
                tiled = "1" if option == 1 else "0"
                
                key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
                win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
                win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, tiled)
                win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)
            
        else: # Linux
            if self.model.image_path is not None:
                wallpaper_option = 'wallpaper' if option == 0 else 'centered'

                call('gconftool-2 -t str -s /desktop/gnome/background/picture_filename'.split() + [path + "/hr_wallpaper.bmp"], stdout=PIPE, stderr=PIPE)
                call('gconftool-2 -t str -s /desktop/gnome/background/picture_options'.split() + [wallpaper_option], stdout=PIPE, stderr=PIPE)
