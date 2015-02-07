#!/usr/bin/env python
# PyQt5
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import QDir, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QFileSystemModel, QGraphicsScene

# Hitagi Reader
from resources.hitagi import Ui_Hitagi

from model.settings import SettingsModel

from controller.canvas import CanvasController
from controller.main import MainController

# Misc
import webbrowser

class MainView(QMainWindow):

    @property
    def include_subfolders(self):
        return self.ui.actionInclude_subfolders.isChecked()
    @include_subfolders.setter
    def include_subfolders(self, value):
        self.ui.actionInclude_subfolders.setChecked(value)

    def __init__(self, model, controller):
        self.settings = SettingsModel()
        self.model = model
        self.canvas = self.model.canvas
        self.main_controller = controller
        self.canvas_controller = CanvasController(self.canvas)
        super(MainView, self).__init__()
        self.build_ui()

        self.model.subscribe_update_func(self.update_ui_from_model)

    def build_ui(self):
        self.ui = Ui_Hitagi()
        self.ui.setupUi(self)

        self.ui.pushButton_change.clicked.connect(self.on_change_directory)

        # File
        self.ui.actionSearch_online.triggered.connect(self.on_close)
        self.ui.actionSet_as_wallpaper.triggered.connect(self.on_wallpaper)
        self.ui.actionCopy_to_clipboard.triggered.connect(self.on_clipboard)
        self.ui.actionOpen_current_directory.triggered.connect(self.on_close)
        self.ui.actionOptions.triggered.connect(self.on_options)
        self.ui.actionExit.triggered.connect(self.on_close)
        # Folder
        self.ui.actionChange_directory.triggered.connect(self.on_change_directory) 
        self.ui.actionInclude_subfolders.triggered.connect(self.on_include_subfolders)

        # View
        self.ui.actionZoom_in.triggered.connect(self.on_zoom_in)
        self.ui.actionZoom_out.triggered.connect(self.on_zoom_out)
        self.ui.actionOriginal_size.triggered.connect(self.on_zoom_original)
        self.ui.actionFit_image_width.triggered.connect(self.on_scale_image_to_width)
        self.ui.actionFit_image_height.triggered.connect(self.on_scale_image_to_height)
        self.ui.actionFile_list.triggered.connect(self.on_toggle_filelist)
        self.ui.actionFullscreen.triggered.connect(self.on_fullscreen)

        # Help
        self.ui.actionChangelog.triggered.connect(self.on_changelog)
        self.ui.actionAbout.triggered.connect(self.on_about)

        # Load stylesheet
        stylesheet_dir = "resources/hitagi.stylesheet"
        with open(stylesheet_dir, "r") as sh:
            self.setStyleSheet(sh.read())

        # File view
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(self.settings.get('Directory', 'default'))

        self.ui.treeView.setModel(self.file_model)
        self.ui.treeView.setRootIndex(self.file_model.index(self.settings.get('Directory', 'default')))
        self.ui.treeView.setColumnWidth(0, 200) 
        self.ui.treeView.setColumnWidth(1, 200)
        self.ui.treeView.hideColumn(1)
        self.ui.treeView.hideColumn(2)

        # Shortcuts
        _translate = QtCore.QCoreApplication.translate
        self.ui.actionExit.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'exit')))

        self.ui.actionChange_directory.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'directory')))

        self.ui.actionZoom_in.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'zoomin')))
        self.ui.actionZoom_out.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'zoomout')))
        self.ui.actionOriginal_size.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'zoomoriginal')))
        self.ui.actionFullscreen.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'fullscreen')))

    # On resize
    def resizeEvent(self, resizeEvent):
        self.main_controller.update_canvas(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image())

    # Additional static shortcuts
    def keyPressEvent(self, e):
        if e.key() == QtGui.QKeySequence(self.settings.get('Hotkeys', 'previmage')):
            self.main_controller.prev_image(self.ui.graphicsView.width(), self.ui.graphicsView.height())
        elif e.key() == QtGui.QKeySequence(self.settings.get('Hotkeys', 'nextimage')):
            self.main_controller.next_image(self.ui.graphicsView.width(), self.ui.graphicsView.height())
        elif e.key() == QtCore.Qt.Key_Escape and self.is_fullscreen:
            self.main_controller.toggle_fullscreen()

    def on_clipboard(self):
        print("")

    def on_wallpaper(self):
        self.main_controller.set_wallpaper()

    def on_zoom_in(self):
        self.canvas_controller.update_canvas(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 1, 1.1)

    def on_zoom_out(self):
        self.canvas_controller.update_canvas(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 1, 0.9)

    def on_zoom_original(self):
        self.canvas_controller.update_canvas(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 4)

    def on_scale_image_to_width(self):
        self.canvas_controller.update_canvas(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 2)

    def on_scale_image_to_height(self):
        self.canvas_controller.update_canvas(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 3)

    def on_toggle_filelist(self):
        if self.ui.actionFile_list.isChecked():
            self.ui.fileWidget.show()
        else:
            self.ui.fileWidget.hide()

    def on_include_subfolders(self):
        self.main_controller.change_include_subfolders(self.include_subfolders)

    def on_fullscreen(self):
        self.main_controller.toggle_fullscreen()

    def on_close(self):
        self.close()

    def on_change_directory(self):
        self.main_controller.change_directory(self.ui.graphicsView.width(), self.ui.graphicsView.height())

    def on_options(self):
        from view.OptionsView import OptionDialog
        self.dialog = OptionDialog(self, None, None)
        self.dialog.show()

    def on_changelog(self):
        webbrowser.open('https://gimu.org/hitagi-reader/docs')

    def on_about(self):
        from view.AboutView import AboutDialog
        dialog = AboutDialog(self, None, None)
        dialog.show()

    def update_ui_from_model(self):
        if self.model.image_index != -1:
            self.ui.treeView.setRootIndex(self.file_model.index(self.model.directory))
            self.ui.statusbar.showMessage(str(self.model.image_paths[self.model.image_index]) + "    " + str(self.model.image_index + 1) + " of " + str(len(self.model.image_paths)))
            self.ui.graphicsView.setScene(self.canvas.scene)

        if self.model.is_fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()

        self.include_subfolders = self.model.include_subfolders
