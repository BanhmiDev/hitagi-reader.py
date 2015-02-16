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

        self.generate_hotkey_list()

        # Global
        self.ui.button_save.clicked.connect(self.close)
        self.ui.button_cancel.clicked.connect(self.close)

        # Hotkey assigning
        self.new_shortcut = QKeySequenceEdit(self.ui.input_new_shortcut)

        self.ui.button_assign.clicked.connect(self.on_new_shortcut)

    def generate_hotkey_list(self):
        for option in self.settings.options('Hotkeys'):
            item = QListWidgetItem()
            item.setText(option)
            item.setData(Qt.UserRole, self.settings.get('Hotkeys', option))
            self.ui.listWidget.addItem(item)

    def on_listWidget_currentItemChanged(self, new, prev):
        if new is not None:
            self.selected_option = new.text()
            self.ui.input_cur_shortcut.setText(new.data(Qt.UserRole))

    def on_new_shortcut(self):
        _new_shortcut = str(QKeySequence.toString(self.new_shortcut.keySequence()))

        self.settings.set('Hotkeys', self.selected_option, _new_shortcut)
        with open('config.ini', 'w') as configfile:
            self.settings.write(configfile)

        # Regenerate list
        self.ui.listWidget.clear()
        self.generate_hotkey_list()

        # Update inputs
        self.ui.input_cur_shortcut.setText(_new_shortcut)
        self.new_shortcut.clear()
