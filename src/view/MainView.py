#!/usr/bin/env python
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import QDir, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QFileSystemModel, QGraphicsScene, QDesktopWidget, QLabel, QShortcut

from resources.hitagi import Ui_Hitagi

from model.settings import SettingsModel

from controller.canvas import CanvasController
from controller.main import MainController

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
        self.center_ui()

        self.model.subscribe_update_func(self.update_ui_from_model)

    def build_ui(self):
        self.ui = Ui_Hitagi()
        self.ui.setupUi(self)

        #self.ui.pushButton_change.clicked.connect(self.on_change_directory)

        # File menu
        self.ui.actionSet_as_wallpaper.triggered.connect(self.on_wallpaper)
        self.ui.actionCopy_to_clipboard.triggered.connect(self.on_clipboard)
        self.ui.actionOpen_current_directory.triggered.connect(self.on_current_dir)
        self.ui.actionOptions.triggered.connect(self.on_options)
        self.ui.actionExit.triggered.connect(self.on_close)

        # Folder menu
        self.ui.actionOpen_next.triggered.connect(self.on_next_image)
        self.ui.actionOpen_previous.triggered.connect(self.on_previous_image)
        self.ui.actionChange_directory.triggered.connect(self.on_change_directory)
        self.ui.actionInclude_subfolders.triggered.connect(self.on_include_subfolders)

        # View menu
        self.ui.actionZoom_in.triggered.connect(self.on_zoom_in)
        self.ui.actionZoom_out.triggered.connect(self.on_zoom_out)
        self.ui.actionOriginal_size.triggered.connect(self.on_zoom_original)
        self.ui.actionFit_image_width.triggered.connect(self.on_scale_image_to_width)
        self.ui.actionFit_image_height.triggered.connect(self.on_scale_image_to_height)
        self.ui.actionFile_list.triggered.connect(self.on_toggle_filelist)
        self.ui.actionFullscreen.triggered.connect(self.on_fullscreen)

        # Help menu
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
        self.ui.actionExit.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Exit')))

        self.ui.actionOpen_next.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Next')))
        self.ui.actionOpen_previous.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Previous')))
        self.ui.actionChange_directory.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Directory')))

        self.ui.actionZoom_in.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Zoom in')))
        self.ui.actionZoom_out.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Zoom out')))
        self.ui.actionOriginal_size.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Zoom original')))
        self.ui.actionFullscreen.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Fullscreen')))
        
    def center_ui(self):
        ui_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        ui_geometry.moveCenter(center_point)
        self.move(ui_geometry.topLeft())

    # On resize
    def resizeEvent(self, resizeEvent):
        self.main_controller.update_canvas(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image())

    # Additional static shortcuts
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape and self.model.is_fullscreen:
            self.main_controller.toggle_fullscreen()

        # Redefine shortcuts when hiding menubar
        if self.model.is_fullscreen and self.model.hide_menubar:
            if e.key() == QKeySequence(self.settings.get('Hotkeys', 'Exit')):
                self.on_close()
            elif e.key() == QKeySequence(self.settings.get('Hotkeys', 'Next')):
                self.on_next_image()
            elif e.key() == QKeySequence(self.settings.get('Hotkeys', 'Previous')):
                self.on_previous_image()
            elif e.key() == QKeySequence(self.settings.get('Hotkeys', 'Directory')):
                self.on_change_directory()
            elif e.key() == QKeySequence(self.settings.get('Hotkeys', 'Zoom in')):
                self.on_zoom_in()
            elif e.key() == QKeySequence(self.settings.get('Hotkeys', 'Zoom out')):
                self.on_zoom_out()
            elif e.key() == QKeySequence(self.settings.get('Hotkeys', 'Zoom original')):
                self.on_zoom_original()
            elif e.key() == QKeySequence(self.settings.get('Hotkeys', 'Fullscreen')):
                self.main_controller.toggle_fullscreen()

    # File menu
    def on_wallpaper(self):
        from view.WallpaperView import WallpaperDialog
        from controller.wallpaper import WallpaperController

        _image = self.model.get_image()
        if _image is not None:
            dialog = WallpaperDialog(self, None, WallpaperController(self.model), _image)
            dialog.show()

    def on_clipboard(self):
        self.main_controller.copy_to_clipboard()

    def on_current_dir(self):
        import subprocess
        # Windows
        subprocess.Popen(r'explorer /select,' + self.model.get_image_path())

    def on_options(self):
        from view.OptionsView import OptionDialog
        self.dialog = OptionDialog(self, None, None)
        self.dialog.show()

    def on_close(self):
        self.close()

    # Folder menu
    def on_next_image(self):
        self.main_controller.next_image(self.ui.graphicsView.width(), self.ui.graphicsView.height())

    def on_previous_image(self):
        self.main_controller.prev_image(self.ui.graphicsView.width(), self.ui.graphicsView.height())

    def on_change_directory(self):
        self.main_controller.change_directory(self.ui.graphicsView.width(), self.ui.graphicsView.height())

    def on_include_subfolders(self):
        self.main_controller.change_include_subfolders(self.include_subfolders)

    # View menu
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

    def on_fullscreen(self):
        self.main_controller.toggle_fullscreen()

    # Help menu
    def on_changelog(self):
        webbrowser.open('https://gimu.org/hitagi-reader/docs')

    def on_about(self):
        from view.AboutView import AboutDialog
        dialog = AboutDialog(self, None, None)
        dialog.show()

    # Update UI from model
    def update_ui_from_model(self):
        # On changing directory
        if self.model.image_index != -1:
            self.ui.treeView.setRootIndex(self.file_model.index(self.model.directory))
            self.ui.statusbar.showMessage(str(self.model.image_paths[self.model.image_index]) + "    " + str(self.model.image_index + 1) + " of " + str(len(self.model.image_paths)))
            self.ui.graphicsView.setScene(self.canvas.scene)

        # Fullscreen mode switching
        if self.model.is_fullscreen:
            self.showFullScreen()
            if self.model.hide_menubar:
                self.ui.menubar.hide()
            if self.model.hide_statusbar:
                self.ui.statusbar.hide()
        else:
            self.showNormal()
            if self.model.hide_menubar:
                self.ui.menubar.show()
            if self.model.hide_statusbar:
                self.ui.statusbar.show()

        self.include_subfolders = self.model.include_subfolders
