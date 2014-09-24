#!/usr/bin/env python
import sys, json, webbrowser
from pathlib import Path

from PySide import QtCore
from PySide.QtGui import QApplication, QMainWindow, QFileDialog, QImage, QPixmap, QMessageBox, QDialog, QLabel, QVBoxLayout

from hitalib.ui.dialog_settings_ui import Ui_Settings
from hitalib.ui.dialog_changelog_ui import Ui_Changelog
from hitalib.ui.dialog_about_ui import Ui_About

class Settings(QDialog, Ui_Settings):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

class Changelog(QDialog, Ui_Changelog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

class Hitagi(QDialog, Ui_About):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

