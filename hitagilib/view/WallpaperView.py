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

        self.scene = QGraphicsScene()

        self.ui.graphicsView.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(self.pixmap_item)
        self.scene.update()

        self.ui.button_set_as_wallpaper.clicked.connect(self.on_set_as_wallpaper)
        self.ui.button_cancel.clicked.connect(self.close)

    def on_set_as_wallpaper(self):
        if self.ui.radio_original_size.isChecked():
            _radio = 0
        elif self.ui.radio_tiled.isChecked():
            _radio = 1
        elif self.ui.radio_fit_to_width.isChecked():
            _radio = 2
        else:
            _radio = 3

        self.controller.set_as_wallpaper(_radio)
