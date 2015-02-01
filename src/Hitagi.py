#!/usr/bin/env python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplashScreen)

from model.app import AppModel
from controller.main import MainController
from view.MainView import MainView

class Hitagi(QMainWindow):
    def __init__(self):
        super(Hitagi, self).__init__()
        self.model = AppModel()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Splash screen
    splash_pix = QPixmap('resources/splash.jpg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Start
    m = Hitagi()

    splash.finish(m)
    sys.exit(app.exec())