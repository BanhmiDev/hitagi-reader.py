#!/usr/bin/env python3
import time

from PyQt5.QtCore import QThread, pyqtSignal

class SlideshowModel(QThread):
    updateSignal = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        self.is_running = True

    def run(self):
        while self.is_running:
            time.sleep(1) # Settings
            self.updateSignal.emit()
