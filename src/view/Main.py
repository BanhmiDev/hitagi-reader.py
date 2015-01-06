from PyQt5 import uic
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QFileSystemModel)

class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.ui = uic.loadUi("resources/hitagi.ui", self)

        self.setWindowTitle('Hitagi Reader 0.5')
        self.setWindowIcon(QIcon('resources/icon.jpg'))

        with open('resources/hitagi.stylesheet', 'r') as sheet:
            self.setStyleSheet(sheet.read())
        self.statusbar.showMessage('Showing directory')

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(QDir.rootPath()))

        
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setStatusTip('Exit Hitagi Reader')

        # Folder
        self.actionChange_directory.setShortcut('Ctrl+D')
        self.actionChange_directory.setStatusTip('Change current directory')

        self.actionInclude_subfolders.setStatusTip('Toggle subfolder fetching')

        # Display
        self.actionFullscreen.setShortcut('F12')
        self.actionFullscreen.setStatusTip('Toggle fullscreen mode')

        # Help
        self.actionChangelog.setStatusTip('Open changelog dialog')
        self.actionAbout.setStatusTip('Open about dialog')

    def options(self):
        from view.Options import OptionDialog
        dialog = OptionDialog()
        dialog.show()

    def changelog(self):
        from view.Changelog import ChangelogDialog
        dialog = ChangelogDialog()
        dialog.show()

    def about(self):
        from view.About import AboutDialog
        dialog = AboutDialog()
        dialog.show()
