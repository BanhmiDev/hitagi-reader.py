#!/usr/bin/env python
from PyQt5.QtCore import Qt

class CanvasController(object):

    def __init__(self, canvas):
        self.canvas = canvas

    def update_canvas(self, container_width, container_height, image = None, scale = 0, factor = 1):
        """Update/scale image in canvas."""
        if image is not None:
            # Scaling options
            # 0: Default mode (ratio scaling)
            # 1: Scale with factor (zoom)
            # 2: Scale to container width
            # 3: Scale to container height
            # 4: Scale to original size
            if scale == 0:
                container_size = (container_width, container_height)
                image_size = (image.width(), image.height())
                ratio = [image_size[0] / container_size[0], image_size[1] / container_size[1]]
                if ratio[0] > 1 and ratio[0] > ratio[1]:
                    image = image.scaledToWidth(container_size[0], Qt.SmoothTransformation)
                elif ratio[1] > 1 and ratio[1] > ratio[0]:
                    image = image.scaledToHeight(container_size[1], Qt.SmoothTransformation)
            elif scale == 1:
                self.canvas.scale_factor *= factor
                image = image.scaled(self.canvas.current_image.width() * self.canvas.scale_factor, self.canvas.current_image.height() * self.canvas.scale_factor, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # Reset scale factor
                self.canvas.scale_factor = 1
            elif scale == 2:
                image = image.scaledToWidth(container_width, Qt.SmoothTransformation)
            elif scale == 3:
                image = image.scaledToHeight(container_height, Qt.SmoothTransformation)
            elif scale == 4:
                image = image

            # Centering and dragging 'fix'
            if image.width() < container_width:
                delta_x = container_width - image.width()
            else:
                delta_x = 0

            full_container_width = image.width() + delta_x * 2
            self.canvas.scene.setSceneRect(-delta_x, 0, full_container_width, image.height())

            # Update to model
            self.canvas.current_image = image
            self.canvas.update()
