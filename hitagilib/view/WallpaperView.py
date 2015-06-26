#!/usr/bin/env python3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsPixmapItem

from hitagilib.ui.wallpaper import Ui_Dialog

class WallpaperDialog(QDialog):

    def __init__(self, parent, model, controller, image):
        self.model = model
        self.controller = controller 
        self.image = image
        super(WallpaperDialog, self).__init__(parent)
        self.build_ui()

    def build_ui(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.button_set_as_wallpaper.clicked.connect(self.on_set_as_wallpaper)
        self.ui.button_cancel.clicked.connect(self.close)

    def on_set_as_wallpaper(self):
        if self.ui.radio_original_size.isChecked():
            radio = 0
        elif self.ui.radio_tiled.isChecked():
            radio = 1
        elif self.ui.radio_fit_to_width.isChecked():
            radio = 2
        else:
            radio = 3

        self.controller.set_as_wallpaper(radio)
        self.close()
