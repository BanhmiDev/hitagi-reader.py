#!/usr/bin/env python
from PyQt5 import uic
from PyQt5.QtCore import (pyqtSlot, QDir)
#!/usr/bin/env python
from controller.canvas import CanvasController

class MainController(object):

    def __init__(self, model):
        self.model = model
        self.canvas = CanvasController(self.model.canvas)

    # called from view class
    def change_include_subfolders(self, checked):
        self.model.include_subfolders = checked
        self.model.announce_update()

    def change_directory(self, container_width, container_height, directory = None):
        """Change current directory."""
        self.model.change_directory(directory)
        image = self.model.get_image()
        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

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

    def prev_image(self, container_width, container_height):
        """Go to previous image."""
        if self.model.image_index > 0:
            self.model.image_index -= 1
        image = self.model.get_image()

        # Use canvas controller
        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    def next_image(self, container_width, container_height):
        """Go to next image."""
        if self.model.image_index < (len(self.model.image_paths) - 1):
            self.model.image_index += 1
        image = self.model.get_image()

        self.canvas.update_canvas(container_width, container_height, image)
        self.model.announce_update()

    def copy_to_clipboard(self):
        if self.model.image_index != -1:
            self.model.clipboard.setImage(self.get_image(), QClipboard.Clipboard)
        