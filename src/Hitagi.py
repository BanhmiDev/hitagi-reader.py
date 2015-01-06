#!/usr/bin/env python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplashScreen)

from model.Model import Model
from controller.MainController import MainController
from view.Main import Main

class Hitagi(QMainWindow):
    def __init__(self):
        super(Hitagi, self).__init__()

        self.controller = MainController()
        self.controller.view.show()

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