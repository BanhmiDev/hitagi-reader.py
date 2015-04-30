#!/usr/bin/env python3
import webbrowser

from PyQt5.QtCore import QTimer, QThread, QDir, Qt, QObject, pyqtSignal, QModelIndex, QCoreApplication
from PyQt5.QtGui import QKeySequence, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QFileSystemModel, QGraphicsScene, QDesktopWidget, QAbstractItemView, QShortcut, QMessageBox

from hitagilib.ui.hitagi import Ui_Hitagi

from hitagilib.model.settings import SettingsModel
from hitagilib.model.slideshow import SlideshowModel
from hitagilib.model.favorites import FavoritesModel
from hitagilib.controller.canvas import CanvasController
from hitagilib.controller.main import MainController

class MainView(QMainWindow):

    def __init__(self, model, controller):
        self.settings = SettingsModel()
        self.slideshow = SlideshowModel()
        self.slideshow.updateSignal.connect(self.on_next_item)

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
        self.ui.actionSlideshow.triggered.connect(self.on_slideshow)

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
        self.file_model.setNameFilters(['*.gif', '*.jpeg', '*.jpg', '*.png'])
        self.file_model.setNameFilterDisables(False)
        self.file_model.setRootPath(self.settings.get('Directory', 'default'))

        self.ui.treeView.setModel(self.file_model)
        self.ui.treeView.setColumnWidth(0, 120)
        self.ui.treeView.setColumnWidth(1, 120)
        self.ui.treeView.hideColumn(1)
        self.ui.treeView.hideColumn(2)

        # Double click
        self.ui.treeView.activated.connect(self.on_dir_list_activated)
        # Update file list
        self.ui.treeView.clicked.connect(self.on_dir_list_clicked)
        # Open parent
        self.ui.pushButton_open_parent.clicked.connect(self.on_open_parent)
        self.ui.pushButton_favorite.clicked.connect(self.on_manage_favorite)

        # Shortcuts
        _translate = QCoreApplication.translate
        self.ui.actionExit.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Exit')))

        self.ui.actionOpen_next.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Next')))
        self.ui.actionOpen_previous.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Previous')))
        self.ui.actionChange_directory.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Directory')))
        self.ui.actionAdd_to_favorites.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Add to favorites')))
        self.ui.actionRemove_from_favorites.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Remove from favorites')))
        self.ui.actionSlideshow.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Slideshow')))

        self.ui.actionZoom_in.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Zoom in')))
        self.ui.actionZoom_out.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Zoom out')))
        self.ui.actionOriginal_size.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Zoom original')))
        self.ui.actionFullscreen.setShortcut(_translate("Hitagi", self.settings.get('Hotkeys', 'Fullscreen')))

        # Load favorites in UI
        self.load_favorites()

        # Background
        self.ui.graphicsView.setBackgroundBrush(QBrush(QColor(self.settings.get('Look', 'background')), Qt.SolidPattern))

        # Save current height for fullscreen mode
        self.default_menubar_height = self.ui.menubar.height()

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
        if e.key() == Qt.Key_Escape and self.model.is_fullscreen:
            self.main_controller.toggle_fullscreen()

    def on_open_parent(self):
        parent_index = self.file_model.parent(self.file_model.index(self.file_model.rootPath()))
        self.file_model.setRootPath(self.file_model.filePath(parent_index))
        self.ui.treeView.setRootIndex(parent_index)

        # Update directory path
        self.model.directory = self.file_model.filePath(parent_index)

        self.update_ui_from_model()

    def on_dir_list_activated(self, index):
        if self.file_model.isDir(index) is not False:
            self.file_model.setRootPath(self.file_model.filePath(index))
            self.ui.treeView.setRootIndex(index)

            # Save current path
            self.model.directory = self.file_model.filePath(index)
            self.update_ui_from_model()
        
    def on_dir_list_clicked(self, index):
        self.main_controller.open_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.file_model.filePath(index))

    # File menu
    def on_set_as_wallpaper(self):
        from hitagilib.view.WallpaperView import WallpaperDialog
        from hitagilib.controller.wallpaper import WallpaperController

        _image = self.model.get_image()
        if _image is not None:
            dialog = WallpaperDialog(self, None, WallpaperController(self.model), _image)
            dialog.show()

    def on_clipboard(self):
        self.main_controller.copy_to_clipboard()

    def on_current_dir(self):
        self.main_controller.open_in_explorer()

    def on_options(self):
        from hitagilib.view.OptionsView import OptionDialog
        self.dialog = OptionDialog(self)
        self.dialog.show()

    def on_close(self):
        if self.slideshow.isRunning():
            self.slideshow.exit()
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

    def on_slideshow(self):
        if self.ui.actionSlideshow.isChecked():
            self.slideshow.start()
            self.slideshow.is_running = True
        else:
            self.slideshow.is_running = False
            self.slideshow.exit()

    def on_change_directory(self):
        self.main_controller.change_directory()

    # View menu
    def on_zoom_in(self):
        self.canvas_controller.scale_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 1.1)

    def on_zoom_out(self):
        self.canvas_controller.scale_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 0.9)

    def on_scale_image_to_width(self):
        self.canvas_controller.update_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 1)

    def on_scale_image_to_height(self):
        self.canvas_controller.update_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 2)

    def on_zoom_original(self):
        self.canvas_controller.update_image(self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.model.get_image(), 3)

    def on_toggle_filelist(self):
        if self.ui.actionFile_list.isChecked():
            self.ui.fileWidget.show()
        else:
            self.ui.fileWidget.hide()

    def on_fullscreen(self):
        self.main_controller.toggle_fullscreen()

    # Favorite button
    def on_manage_favorite(self):
        if self.main_controller.check_favorites(self.model.directory):
            self.on_remove_from_favorites()
        else:
            self.on_add_to_favorites()

    # Favorite menu
    def on_add_to_favorites(self):
        self.main_controller.add_to_favorites()
        self.load_favorites()
        self.update_ui_from_model()

    def on_remove_from_favorites(self):
        self.main_controller.remove_from_favorites()
        self.load_favorites()
        self.update_ui_from_model()

    # Help menu
    def on_changelog(self):
        webbrowser.open('https://gimu.org/hitagi-reader/docs')

    def on_about(self):
        from hitagilib.view.AboutView import AboutDialog
        dialog = AboutDialog(self, None, None)
        dialog.show()

    def show_explorer_error(self):
        notify = QMessageBox()
        notify.setWindowTitle("Error")
        notify.setText("Couldn't open the current directory with an appropriate filemanager!")
        notify.exec_()

    def update_ui_from_model(self):
        """Update UI from model."""
        self.settings = SettingsModel()

        # On changing directory
        self.file_model.setRootPath(self.model.directory)
        self.ui.treeView.setRootIndex(self.file_model.index(self.model.directory))

        # Update favorite button
        if self.main_controller.check_favorites(self.model.directory):
            self.ui.pushButton_favorite.setText("Unfavorite")
        else:
            self.ui.pushButton_favorite.setText("Favorite")

        # Canvas update
        self.ui.graphicsView.setScene(self.canvas.scene)

        # Fullscreen mode switching
        if self.model.is_fullscreen:
            self.showFullScreen()
            if self.settings.get('Misc', 'hide_menubar') == 'True':
                self.ui.menubar.setMaximumHeight(0) # Workaround to preserve shortcuts
        else:
            self.showNormal()
            if self.settings.get('Misc', 'hide_menubar') == 'True':
                self.ui.menubar.setMaximumHeight(self.default_menubar_height)
