#!/usr/bin/env python3
from pathlib import Path

from PyQt5.QtGui import QImage, QClipboard
from PyQt5.QtWidgets import QFileDialog

from hitagilib.model.settings import SettingsModel
from hitagilib.model.favorites import FavoritesModel
from hitagilib.controller.canvas import CanvasController

class MainController(object):

    def __init__(self, model):
        self.settings = SettingsModel()
        self.favorites = FavoritesModel()
        self.model = model
        self.canvas = CanvasController(self.model.canvas)

        self.start()

    def start(self):
        """Initial calls."""
        self.change_directory(self.settings.get('Directory', 'default'))

    def change_directory(self, directory = None):
        """Change current directory."""
        if not directory:
            new_directory = QFileDialog.getExistingDirectory(None, "Change current directory", '/')
        else:
            new_directory = directory

        # Error suppression
        if not new_directory:
            return

        self.model.directory = new_directory
        self.model.announce_update()

    def check_favorites(self, directory):
        return self.favorites.check_favorites(directory)

    def add_to_favorites(self):
        """Favorite current directory."""
        self.favorites.add(str(self.model.directory))
        self.favorites.save()

    def remove_from_favorites(self):
        """Remove current directory from favorite list."""
        self.favorites.remove(str(self.model.directory))
        self.favorites.save()

    def toggle_fullscreen(self):
        """Toggle between fullscreen mode."""
        if self.model.is_fullscreen:
            self.model.is_fullscreen = False
        else:
            self.model.is_fullscreen = True

        # Update UI
        self.model.announce_update()

    def update_canvas(self, image = None):
        """Update canvas with image."""
        self.canvas.update_image(self.settings.getint('Viewport', 'selection'), image)
        self.model.announce_update()

    def open_image(self, path):
        """Open specific image via path."""
        image = QImage(str(path))
        if image.isNull():
            image = None
            
        self.model.image_path = path
        self.canvas.update_image(self.settings.getint('Viewport', 'selection'), image)

    def copy_to_clipboard(self):
        """Open current image to clipboard."""
        if self.model.image_path is not None:
            self.model.clipboard.setImage(self.model.get_image(), QClipboard.Clipboard)

    def open_in_explorer(self):
        """Open current directory in an explorer environment."""
        import os, subprocess
        path = self.model.get_directory()

        # Todo: let user choose his filemanager?
        if path is not None:
            if os.name == 'nt': # Windows
                try:
                    subprocess.Popen(r'explorer /select,' + path)
                except:
                    pass
            else: # Other OS
                try:
                    return subprocess.call(['thunar', path])
                except:
                    pass
                try:
                    return subprocess.call(['nautilus', path])
                except:
                    pass
                try:
                    return subprocess.call(['xfe', path])
                except:
                    pass

            self.show_explorer_error()
        
