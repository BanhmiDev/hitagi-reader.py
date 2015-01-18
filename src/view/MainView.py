from PyQt5 import uic, QtCore
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import (QMainWindow, QFileSystemModel)

from resources.hitagi import Ui_MainWindow

class MainView(QMainWindow):

    @property
    def include_subfolders(self):
        return self.ui.actionInclude_subfolders.isChecked()
    @include_subfolders.setter
    def include_subfolders(self, value):
        self.ui.actionInclude_subfolders.setChecked(value)

    def __init__(self, model, main_controller):
        self.model = model
        self.main_controller = main_controller
        super(MainView, self).__init__()
        self.build_ui()

        self.model.subscribe_update_func(self.update_ui_from_model)

    def build_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Actions
        self.ui.actionSearch_online.triggered.connect(self.on_close)
        self.ui.actionSet_as_wallpaper.triggered.connect(self.on_wallpaper)
        self.ui.actionCopy_to_clipboard.triggered.connect(self.on_clipboard)
        self.ui.actionOpen_current_directory.triggered.connect(self.on_close)
        self.ui.actionOptions.triggered.connect(self.on_options)
        self.ui.actionExit.triggered.connect(self.on_close)
        self.ui.actionChange_directory.triggered.connect(self.on_change_directory)
        self.ui.actionInclude_subfolders.triggered.connect(self.on_include_subfolders)
        self.ui.actionFullscreen.triggered.connect(self.on_fullscreen)
        self.ui.actionChangelog.triggered.connect(self.on_changelog)
        self.ui.actionAbout.triggered.connect(self.on_about)

        sshFile="resources/hitagi.stylesheet"
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())

        self.ui.splitter.setSizes([80, 100])

        self.ui.treeView.setModel(self.file_model)
        self.ui.treeView.setRootIndex(self.file_model.index(QDir.rootPath()))
        self.ui.treeView.setColumnWidth(0, 200) 
        self.ui.treeView.setColumnWidth(1, 200)
        self.ui.treeView.hideColumn(1)
        self.ui.treeView.hideColumn(2)

    # on resize
    def resizeEvent(self, resizeEvent):
        self.main_controller.update_canvas(self.ui.label.width(), self.ui.label.height())

    # key shortcuts
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Left:
            self.main_controller.prev_image(self.ui.label.width(), self.ui.label.height())
        elif e.key() == QtCore.Qt.Key_Right:
            self.main_controller.next_image(self.ui.label.width(), self.ui.label.height())
        elif e.key() == QtCore.Qt.Key_D:
            self.main_controller.change_directory(self.ui.label.width(), self.ui.label.height())
        elif e.key() == QtCore.Qt.Key_F:
            self.main_controller.toggle_fullscreen()
        elif e.key() == QtCore.Qt.Key_Escape and self.is_fullscreen:
            self.main_controller.toggle_fullscreen()

    def on_clipboard(self):
        print("2")
    def on_wallpaper(self):
        print("2")

    def on_include_subfolders(self):
        self.main_controller.change_include_subfolders(self.include_subfolders)

    def on_fullscreen(self):
        self.main_controller.toggle_fullscreen()

    def on_close(self):
        self.close()

    def on_change_directory(self):
        self.main_controller.change_directory(self.ui.label.width(), self.ui.label.height())

    def on_options(self):
        from view.OptionsView import OptionDialog
        self.dialog = OptionDialog(self, None, None)
        self.dialog.show()

    def on_changelog(self):
        from view.ChangelogView import ChangelogDialog
        dialog = ChangelogDialog(self, None, None)
        dialog.show()

    def on_about(self):
        from view.AboutView import AboutDialog
        dialog = AboutDialog(self, None, None)
        dialog.show()


    def update_ui_from_model(self):
        if self.model.image_index != -1:
            self.ui.treeView.setRootIndex(self.file_model.index(self.model.directory))
            #self.ui.statusbar.showMessage(str(self.image_paths[self.image_index]) + "    " + str(self.image_index + 1) + " of " + str(len(self.image_paths)))
            self.ui.label.setPixmap(QPixmap.fromImage(self.model.image))

        if self.model.is_fullscreen:

            self.showFullScreen()
        else:
            self.showNormal()

        self.include_subfolders = self.model.include_subfolders
