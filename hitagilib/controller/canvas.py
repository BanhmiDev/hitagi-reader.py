#!/usr/bin/env python3
from PyQt5.QtCore import Qt

class CanvasController(object):

    def __init__(self, canvas):
        self.canvas = canvas
    
    def update(self, container_width, container_height):
        """Update canvas container geometry."""
        self.canvas.setGeometry(container_width, container_height)

    def update_image(self, selection = 0, image = None):
        """Update image in canvas."""
        if image is not None: # Set image if available (most likely when opening an image)
            self.canvas.set_image(image)
            
        self.canvas.update_image(selection)

    def scale_image(self, factor = 0):
        """Scales image in canvas."""
        self.canvas.scale_image(factor)
    
    def rotate_image(self):
        """Rotate by 90 degrees (clockwise)."""
        self.canvas.rotate_image()

    def flip_image(self, direction):
        """Flip current image."""
        if direction == 0:
            # Horizontal
            self.canvas.flip_image(0)
        else:
            # Vertical
            self.canvas.flip_image(1)
