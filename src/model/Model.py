#!/usr/bin/env python
from PyQt5 import uic
from PyQt5.QtCore import (pyqtSlot, QDir)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtWidgets import (QApplication, QFileSystemModel, QFileDialog)

class Model(object):

    def changeDirectory(self, directory=None):
        """Open file dialog to choose images directory."""

    def toggleFullscreen(self):
        """Toggle into fullscreen mode."""
