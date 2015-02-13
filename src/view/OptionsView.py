#!/usr/bin/env python
from PyQt5.QtWidgets import QDialog, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from model.settings import SettingsModel

from resources.options import Ui_Dialog

class OptionDialog(QDialog):

    def __init__(self, parent, model, controller):
        self.settings = SettingsModel()
        self.model = model
        self.controller = controller
        super(OptionDialog, self).__init__(parent)
        self.build_ui()

    def build_ui(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Layout
        self.ui.lineEdit.setText(self.settings.get('Directory', 'default'))
        self.ui.lineEdit_2.setText(self.settings.get('Look', 'background'))

        # Hotkeys
        for option in self.settings.options('Hotkeys'):
            item = QListWidgetItem()
            item.setText(option)
            item.setData(Qt.UserRole, self.settings.get('Hotkeys', option))
            self.ui.listWidget.addItem(item)

        # Global
        self.ui.button_save.clicked.connect(self.close)
        self.ui.button_cancel.clicked.connect(self.close)

    def on_listWidget_currentItemChanged(self, new, prev):
        self.ui.input_cur_shortcut.setText(new.data(Qt.UserRole))
