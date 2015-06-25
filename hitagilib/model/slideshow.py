#!/usr/bin/env python3
import time

from PyQt5.QtCore import QThread, pyqtSignal

from hitagilib.model.settings import SettingsModel

class SlideshowModel(QThread):
    updateSignal = pyqtSignal()
    restartSignal = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        self.is_running = True
        self.settings = SettingsModel()
        self.speed = self.settings.getint('Slideshow', 'speed') # Get intervals from settings (seconds)

    def run(self):
        while self.is_running:
            time.sleep(self.speed)
            
            self.updateSignal.emit()
