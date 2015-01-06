#!/usr/bin/env python
from PyQt5 import uic
from PyQt5.QtCore import (pyqtSlot, QDir)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileSystemModel)

from model.Model import Model
from view.Main import Main

class MainController(object):

    def __init__(self):
        self.model = Model()
        self.view = Main()

        # File
        self.view.actionSearch_online.triggered.connect(self.view.close)
        self.view.actionSet_as_wallpaper.triggered.connect(self.view.close)
        self.view.actionCopy_to_clipboard.triggered.connect(self.view.close)
        self.view.actionOpen_current_directory.triggered.connect(self.view.close)
        self.view.actionOptions.triggered.connect(self.view.options)
        self.view.actionExit.triggered.connect(self.view.close)

        # Folder
        self.view.actionChange_directory.triggered.connect(self.model.changeDirectory)
        self.view.actionInclude_subfolders.triggered.connect(self.view.close)

        # Display
        self.view.actionFullscreen.triggered.connect(self.model.toggleFullscreen)

        # Help
        self.view.actionChangelog.triggered.connect(self.model.toggleFullscreen)
        self.view.actionAbout.triggered.connect(self.model.toggleFullscreen)