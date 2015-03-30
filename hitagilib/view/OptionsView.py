#!/usr/bin/env python3
from PyQt5.QtGui import QKeySequence, QBrush, QColor
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QKeySequenceEdit, QMessageBox
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
        self.ui.pushButton_browse_directory.clicked.connect(self.on_update_default_directory)
        self.ui.lineEdit_default_directory.setText(self.model.get('Directory', 'default'))

        self.ui.lineEdit_background_color.setText(self.model.get('Look', 'background'))
        self.ui.pushButton_colorpicker.clicked.connect(self.on_update_background)
        
        self.generate_checkbox_list()
        self.generate_hotkey_list()

        # Set viewport behaviour
        self.ui.comboBox_default_viewport.setCurrentIndex(self.model.getint('Viewport', 'selection'))

        # Global
        self.ui.pushButton_save.clicked.connect(self.on_save)
        self.ui.pushButton_cancel.clicked.connect(self.close)

        # Hotkey assigning
        self.new_shortcut = QKeySequenceEdit(self.ui.lineEdit_new_shortcut)
        self.ui.pushButton_assign_hotkey.clicked.connect(self.on_new_shortcut)
        self.ui.pushButton_reset.clicked.connect(self.controller.load_defaults)

    def generate_checkbox_list(self):
        self.ui.checkBox_check_updates.setChecked(self.model.get('Misc', 'check_updates') == 'True')
        self.ui.checkBox_hide_menubar.setChecked(self.model.get('Misc', 'hide_menubar') == 'True')

    def generate_hotkey_list(self):
        for option in self.model.options('Hotkeys'):
            item = QListWidgetItem()
            item.setText(option)
            item.setData(Qt.UserRole, self.model.get('Hotkeys', option))
            self.ui.listWidget_hotkey.addItem(item)

    def on_update_default_directory(self):
        self.controller.update_default_directory()
        self.ui.lineEdit_default_directory.setText(self.model.get('Directory', 'default'))
        
    def on_update_background(self):
        self.controller.update_background()
        self.ui.lineEdit_background_color.setText(self.model.get('Look', 'background'))

    def on_listWidget_hotkey_currentItemChanged(self, new, prev):
        if new is not None:
            self.selected_option = new.text()
            self.ui.lineEdit_current_shortcut.setText(new.data(Qt.UserRole))

    def on_new_shortcut(self):
        _new_shortcut = str(QKeySequence.toString(self.new_shortcut.keySequence()))
        self.controller.update_hotkey(self.selected_option, _new_shortcut)

        # Regenerate list
        self.ui.listWidget_hotkey.clear()
        self.generate_hotkey_list()

        # Update inputs
        self.ui.lineEdit_current_shortcut.setText(_new_shortcut)
        self.new_shortcut.clear()

    def on_checkBox_check_updates_stateChanged(self, state):
        self.controller.update_boolean('check_updates', state)

    def on_checkBox_hide_menubar_stateChanged(self, state):
        self.controller.update_boolean('hide_menubar', state)

    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.controller.update_viewport_behaviour(index)

    @pyqtSlot(int)
    def on_listWidget_locale_currentRowChanged(self, index):
        self.controller.update_locale(index)

    def on_save(self):
        self.controller.apply_settings()
        self.parent.ui.graphicsView.setBackgroundBrush(QBrush(QColor(self.model.get('Look', 'background')), Qt.SolidPattern))
        self.parent.model.announce_update() # Todo: dynamic config changes?
        self.close()

        notify = QMessageBox()
        notify.setWindowTitle("Configuration saved")
        notify.setText("Some changes only take effect after restarting the application.")
        notify.exec_()

    def update_ui_from_model(self):
        self.ui.pushButton_save.setEnabled(True)
