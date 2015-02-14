#!/usr/bin/env python
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QKeySequenceEdit
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

        # Hotkey assigning
        self.new_shortcut = QKeySequenceEdit(self.ui.input_new_shortcut)

        self.ui.button_assign.clicked.connect(self.on_new_shortcut)

    def on_listWidget_currentItemChanged(self, new, prev):
        self.ui.input_cur_shortcut.setText(new.data(Qt.UserRole))

    def on_new_shortcut(self):
        self.settings.set('Hotkeys', 'Exit', str(QKeySequence.toString(self.new_shortcut.keySequence())))
        with open('config.ini', 'w') as configfile:
            self.settings.write(configfile)
