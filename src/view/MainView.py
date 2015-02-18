#!/usr/bin/env python
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import QDir, Qt, QObject, pyqtSignal, QModelIndex
from PyQt5.QtGui import QIcon, QPixmap, QImage, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QFileSystemModel, QGraphicsScene, QDesktopWidget, QLabel, QShortcut, QAbstractItemView, QAction

from resources.hitagi import Ui_Hitagi

from model.settings import SettingsModel
from model.favorites import FavoritesModel
from controller.canvas import CanvasController
from controller.main import MainController

import webbrowser

class MainView(QMainWindow):

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

        # File menu
        self.ui.actionSet_as_wallpaper.triggered.connect(self.on_set_as_wallpaper)
        self.ui.actionCopy_to_clipboard.triggered.connect(self.on_clipboard)
        self.ui.actionOpen_current_directory.triggered.connect(self.on_current_dir)
        self.ui.actionOptions.triggered.connect(self.on_options)
        self.ui.actionExit.triggered.connect(self.on_close)

        # Folder menu
        self.ui.actionOpen_next.triggered.connect(self.on_next_item)
        self.ui.actionOpen_previous.triggered.connect(self.on_previous_item)
        self.ui.actionChange_directory.triggered.connect(self.on_change_directory)

        # View menu
        self.ui.actionZoom_in.triggered.connect(self.on_zoom_in)
        self.ui.actionZoom_out.triggered.connect(self.on_zoom_out)
        self.ui.actionOriginal_size.triggered.connect(self.on_zoom_original)
        self.ui.actionFit_image_width.triggered.connect(self.on_scale_image_to_width)
        self.ui.actionFit_image_height.triggered.connect(self.on_scale_image_to_height)
        self.ui.actionFile_list.triggered.connect(self.on_toggle_filelist)
        self.ui.actionFullscreen.triggered.connect(self.on_fullscreen)

        # Favorite menu
        self.ui.actionAdd_to_favorites.triggered.connect(self.on_add_to_favorites)
        self.ui.actionRemove_from_favorites.triggered.connect(self.on_remove_from_favorites)

        # Help menu
        self.ui.actionChangelog.triggered.connect(self.on_changelog)
        self.ui.actionAbout.triggered.connect(self.on_about)

        # Load stylesheet
        stylesheet_dir = "resources/hitagi.stylesheet"
        with open(stylesheet_dir, "r") as sh:
            self.setStyleSheet(sh.read())
        
        # File listing
        self.file_model = QFileSystemModel()
        self.file_model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.file_model.setNameFilters(['*.jpg', '*.png', '*.jpeg'])
        self.file_model.setNameFilterDisables(False)
        self.file_model.setRootPath(self.settings.get('Directory', 'default'))

        self.ui.treeView.setModel(self.file_model)
        self.ui.treeView.setColumnWidth(0, 200) 
        self.ui.treeView.setColumnWidth(1, 200)
        self.ui.treeView.hideColumn(1)
        self.ui.treeView.hideColumn(2)

        # Double click
        self.ui.treeView.activated.connect(self.on_dir_list_activated)
        # Update file list
        self.ui.treeView.clicked.connect(self.on_dir_list_clicked)
        # Open parent
        self.ui.button_open_parent.clicked.connect(self.on_open_parent)

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
        
        # Load favorites in UI
        self.load_favorites()

    def load_favorites(self):
        self.favorites = FavoritesModel()
        self.ui.menuFavorites.clear()
        for item in self.favorites.items():
            self.ui.menuFavorites.addAction(item).triggered.connect((lambda item: lambda: self.on_open_favorite(item))(item))

    def on_open_favorite(self, path):
        self.main_controller.change_directory(path)

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
                self.on_next_item()
            elif e.key() == QKeySequence(self.settings.get('Hotkeys', 'Previous')):
                self.on_previous_item()
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

    def on_open_parent(self):
        parent_index = self.file_model.parent(self.file_model.index(self.file_model.rootPath()))
        self.file_model.setRootPath(self.file_model.filePath(parent_index))
        self.ui.treeView.setRootIndex(parent_index)

        # Update directory path
        self.model.directory = self.file_model.filePath(parent_index)

    def on_dir_list_activated(self, index):
        if self.file_model.hasChildren(index) is not False:
            self.file_model.setRootPath(self.file_model.filePath(index))
            self.ui.treeView.setRootIndex(index)

            # Save current path
            self.model.directory = self.file_model.filePath(index)
        
    def on_dir_list_clicked(self, index):
        self.main_controller.open_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.file_model.filePath(index))

    # File menu
    def on_set_as_wallpaper(self):
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
        self.dialog = OptionDialog(self)
        self.dialog.show()

    def on_close(self):
        self.close()

    # Folder menu
    def on_next_item(self):
        index = self.ui.treeView.moveCursor(QAbstractItemView.MoveDown, Qt.NoModifier)
        self.ui.treeView.setCurrentIndex(index)
        self.main_controller.open_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.file_model.filePath(index))

    def on_previous_item(self):
        index = self.ui.treeView.moveCursor(QAbstractItemView.MoveUp, Qt.NoModifier)
        self.ui.treeView.setCurrentIndex(index)
        self.main_controller.open_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.file_model.filePath(index))

    def on_change_directory(self):
        self.main_controller.change_directory()

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

    # Favorite menu
    def on_add_to_favorites(self):
        self.main_controller.add_to_favorites()
        self.load_favorites()

    def on_remove_from_favorites(self):
        self.main_controller.remove_from_favorites()
        self.load_favorites()

    # Help menu
    def on_changelog(self):
        webbrowser.open('https://gimu.org/hitagi-reader/docs')

    def on_about(self):
        from view.AboutView import AboutDialog
        dialog = AboutDialog(self, None, None)
        dialog.show()

    def update_ui_from_model(self):
        """Update UI from model."""
        # On changing directory
        self.file_model.setRootPath(self.model.directory)
        self.ui.treeView.setRootIndex(self.file_model.index(self.model.directory))

        #if self.model.image_path is not None:
           # self.ui.statusbar.showMessage(str(self.model.image_path) + "    " + str(self.model.image_index + 1) + " of " + str(len(self.model.image_paths)))
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
