#!/usr/bin/env python
import sys, json, webbrowser
from pathlib import Path

from PySide import QtCore
from PySide.QtGui import QApplication, QMainWindow, QFileDialog, QImage, QPixmap, QMessageBox, QDialog, QLabel, QVBoxLayout, QIcon, QFileSystemModel

from hitalib import Model, Dialogs

__version__ = "1.0"

from hitalib.ui.hitagi_ui import Ui_Mainwindow

class MainWindow(QMainWindow, Ui_Mainwindow):
    resizeCompleted = QtCore.Signal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.dirmodel = QFileSystemModel()
        self.dirmodel.setRootPath("")
        self.dirmodel.setNameFilters(["*.png"]);
        self.dirmodel.setNameFilterDisables(False)
        self.treeView.setModel(self.dirmodel)
        self.treeView.setIndentation(10);
        self.treeView.setRootIndex(self.dirmodel.index(QtCore.QDir.currentPath()))
        self.treeView.hideColumn(1)

        self.splitter_2.splitterMoved.connect(self.updateImage);

        """
        self.stylesheet = "assets/hitagi.stylesheet"
        with open(self.stylesheet, "r") as fh:
            self.setStyleSheet(fh.read())
        """

        self.headerContainer.setText("Hitagi Reader " + __version__)

        self.logoContainer.setPixmap(QPixmap("assets/logo.png"))

        self._resize_timer = None
        self.resizeCompleted.connect(self.handleResizeCompleted)

        # File
        self.actionSearch_online.triggered.connect(self.showSearchOnline)
        self.actionOptions.triggered.connect(self.showOptions)
        self.actionExit.triggered.connect(self.close)
        # Folder
        self.actionOpen_Directory.triggered.connect(self.changeDirectory)
        # Display
        self.actionFullscreen.triggered.connect(self.toggleFullscreen)
        # Help
        self.actionDialog_Changelog.triggered.connect(self.aboutChangelog)
        self.actionDialog_About.triggered.connect(self.aboutHitagi)

        # variables
        self.image_index = -1 # index of current shown image
        self.is_fullscreen = False # fullscreen mode
        self.image_paths = [] # list of images in the chosen directory

        # settings variables
        self.settings_file = u"settings.json" # filename
        self.settings = {
            "currentDir": u"./",
            "hotkeys": ""
        }

        # window properties
        self.is_maximized = self.isMaximized()
        self.window_dimensions = self.geometry()

    def showSearchOnline(self):
        webbrowser.open("https://images.google.com/imghp", 2) 

    def showOptions(self):
        Dialogs.Settings(self).show()

    def aboutChangelog(self):
        Dialogs.Changelog(self).show()

    def aboutHitagi(self):
        Dialogs.Hitagi(self).show()

    def updateResizeTimer(self, interval=None):
        if self._resize_timer is not None:
            self.killTimer(self._resize_timer)
        if interval is not None:
            self._resize_timer = self.startTimer(interval)
        else:
            self._resize_timer = None

    def resizeEvent(self, event):
        self.updateResizeTimer(300)

    def timerEvent(self, event):
        if event.timerId() == self._resize_timer:
            self.updateResizeTimer()
            self.resizeCompleted.emit()

    def handleResizeCompleted(self):
        if self.image_index != -1:
            self.updateImage()

    def keyPressEvent(self, e):
        """Handle available keyboard shortcuts."""
        if e.key() == QtCore.Qt.Key_Left:
            self.prevImage()
        elif e.key() == QtCore.Qt.Key_Right:
            self.nextImage()
        elif e.key() == QtCore.Qt.Key_D:
            self.changeDirectory()
        elif e.key() == QtCore.Qt.Key_F:
            self.toggleFullscreen()
        elif e.key() == QtCore.Qt.Key_Escape and self.is_fullscreen:
            self.toggleFullscreen()

    def changeDirectory(self):
        """Open file dialog to choose images directory."""
        new_directory = QFileDialog.getExistingDirectory(self, self.tr("Choose directory"), self.settings['currentDir'])

        # if canceled, return nothing
        if not new_directory:
            return

        self.image_index = -1

        # subfolder management
        if self.actionSubfolder.isChecked():
            self.image_paths = [i for i in Path(new_directory).rglob("*") if i.suffix.lower() in ['.jpg', '.png']]
        else:
            self.image_paths = [i for i in Path(new_directory).glob("*") if i.suffix.lower() in ['.jpg', '.png']]

        if len(self.image_paths) > 0:
            self.nextImage()
            self.settings['currentDir'] = new_directory;
            self.saveSettings()
        else:
            QMessageBox.information(self, "No Images", "No images were found in '" + new_directory + "'.\nChoose another directory.")

    def updateImage(self):
        """Display and update image."""

        if self.image_index != -1:
            self.setWindowTitle("Hitagi - " + str(self.image_paths[self.image_index]) + "    " + str(self.image_index + 1) + " of " + str(len(self.image_paths)))
            image = QImage(str(self.image_paths[self.image_index]))
            self.statusBar.showMessage(str(self.image_paths[self.image_index]) + "    " + str(self.image_index + 1) + " of " + str(len(self.image_paths)))
            image = QImage(str(self.image_paths[self.image_index]))
            container_size = (self.imageContainer.width(), self.imageContainer.height())

            image_size = (image.width(), image.height())
            ratio = [image_size[0] / container_size[0], image_size[1] / container_size[1]]

            if ratio[0] > 1 and ratio[0] > ratio[1]:
                image = image.scaledToWidth(container_size[0], QtCore.Qt.SmoothTransformation)

            elif ratio[1] > 1 and ratio[1] > ratio[0]:
                image = image.scaledToHeight(container_size[1], QtCore.Qt.SmoothTransformation)

            self.imageContainer.setPixmap(QPixmap.fromImage(image))

    def prevImage(self):
        """Display previous image."""
        if self.image_index > 0:
            self.image_index = self.image_index - 1;
            self.updateImage()

    def nextImage(self):
        """Display next image."""
        if self.image_index < len(self.image_paths) - 1:
            self.image_index = self.image_index + 1;
            self.updateImage()

    def toggleFullscreen(self):
        """Toggle into fullscreen mode."""
        # if already in fullscreen mode
        if self.is_fullscreen: 

            # update image dimension
            self.updateImage()
            self.is_fullscreen = False
            self.actionFullscreen.setChecked(False)

            if self.is_maximized:
                self.showMaximized()
            else:
                self.showNormal()
                self.setGeometry(self.window_dimensions)

        # else NOT in fullscreen mode
        else: 
            if self.image_index == -1:
                #QMessageBox.information(self, "Error", "Open or select a directory first before entering fullscreen mode.")
                return
            else:
                # save properties to restore later on
                self.window_dimensions = self.geometry()
                self.is_maximized = self.isMaximized()

                self.showFullScreen()
                self.is_fullscreen = True
                self.actionFullscreen.setChecked(True)

    def saveSettings(self):
        """Save various data to settings.json."""
        new_settings_file = open(self.settings_file, mode="w")
        json.dump(self.settings, new_settings_file, indent = 4)
        new_settings_file.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hitagi = MainWindow()
    hitagi.show()
    app.exec_()