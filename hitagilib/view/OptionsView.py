#!/usr/bin/env python3
from PyQt5.QtGui import QKeySequence, QBrush, QColor
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QKeySequenceEdit
from PyQt5.QtCore import Qt, pyqtSlot

from hitagilib.model.settings import SettingsModel
from hitagilib.controller.settings import SettingsController

from hitagilib.ui.options import Ui_Dialog

class OptionDialog(QDialog):

    def __init__(self, parent):
        self.model = SettingsModel()
        self.controller = SettingsController(self.model)
        self.parent = parent
        super(OptionDialog, self).__init__(parent)
        self.build_ui()

        self.model.subscribe_update_func(self.update_ui_from_model)

    def build_ui(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Layout
        self.ui.button_browse_directory.clicked.connect(self.on_update_default_directory)
        self.ui.input_default_directory.setText(self.model.get('Directory', 'default'))

        self.ui.input_background_color.setText(self.model.get('Look', 'background'))
        self.ui.button_colorpicker.clicked.connect(self.on_update_background)
        
        self.generate_checkbox_list()
        self.generate_hotkey_list()

        # Set viewport behaviour
        self.ui.comboBox.setCurrentIndex(self.model.getint('Viewport', 'selection'))

        # Global
        self.ui.button_save.clicked.connect(self.on_save)
        self.ui.button_cancel.clicked.connect(self.close)

        # Hotkey assigning
        self.new_shortcut = QKeySequenceEdit(self.ui.input_new_shortcut)
        self.ui.button_assign.clicked.connect(self.on_new_shortcut)
        self.ui.button_reset.clicked.connect(self.controller.load_defaults)

    def generate_checkbox_list(self):
        self.ui.checkbox_check_updates.setChecked(self.model.get('Misc', 'check_updates') == 'True')
        self.ui.checkbox_hide_menubar.setChecked(self.model.get('Misc', 'hide_menubar') == 'True')

    def generate_hotkey_list(self):
        for option in self.model.options('Hotkeys'):
            item = QListWidgetItem()
            item.setText(option)
            item.setData(Qt.UserRole, self.model.get('Hotkeys', option))
            self.ui.listWidget.addItem(item)

    def on_update_default_directory(self):
        self.controller.update_default_directory()
        self.ui.input_default_directory.setText(self.model.get('Directory', 'default'))
        
    def on_update_background(self):
        self.controller.update_background()
        self.ui.input_background_color.setText(self.model.get('Look', 'background'))

    def on_listWidget_currentItemChanged(self, new, prev):
        if new is not None:
            self.selected_option = new.text()
            self.ui.input_cur_shortcut.setText(new.data(Qt.UserRole))

    def on_new_shortcut(self):
        _new_shortcut = str(QKeySequence.toString(self.new_shortcut.keySequence()))
        self.controller.update_hotkey(self.selected_option, _new_shortcut)

        # Regenerate list
        self.ui.listWidget.clear()
        self.generate_hotkey_list()

        # Update inputs
        self.ui.input_cur_shortcut.setText(_new_shortcut) # possible self.model.get('Hotkeys', self.selected_option)
        self.new_shortcut.clear()

    def on_checkbox_check_updates_stateChanged(self, state):
        self.controller.update_boolean('check_updates', state)

    def on_checkbox_hide_menubar_stateChanged(self, state):
        self.controller.update_boolean('hide_menubar', state)

    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.controller.update_viewport_behaviour(index)

    def on_save(self):
        self.controller.apply_settings()
        self.parent.ui.graphicsView.setBackgroundBrush(QBrush(QColor(self.model.get('Look', 'background')), Qt.SolidPattern))
        self.parent.model.announce_update() # Todo: dynamic config changes
        self.close()

    def update_ui_from_model(self):
        self.ui.button_save.setEnabled(True)
