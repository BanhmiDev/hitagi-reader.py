#!/usr/bin/env python3
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog, QFileDialog

class SettingsController(object):

    def __init__(self, model):
        self.model = model

    def update_default_directory(self, directory = None):
        """Change default directory."""
        if not directory:
            new_directory = QFileDialog.getExistingDirectory(None, "Change default directory", '/')
        else:
            new_directory = directory

        if not new_directory:
            return

        self.model.set('Directory', 'default', str(new_directory))
        self.model.announce_update()

    def update_hotkey(self, selected_option, new_shortcut):
        """Update choosen hotkey."""
        self.model.set('Hotkeys', selected_option, new_shortcut)
        self.model.announce_update()

    def update_background(self):
        """Update background via colorpicker."""
        color = QColorDialog().getColor()
        self.model.set('Look', 'background', str(color.name(QColor.HexRgb)))
        self.model.announce_update()

    def update_boolean(self, parent, option, state):
        """Handle switches."""
        state = True if state == 2 else False
        self.model.set(parent, option, str(state))
        self.model.announce_update()

    def update_viewport_behaviour(self, index):
        """Handle default image presentation."""
        if index >= 0:
            self.model.set('Viewport', 'selection', str(index))
            self.model.announce_update()

    def update_slideshow_speed(self, value):
        if value >= 1:
            self.model.set('Slideshow', 'speed', str(value))
            self.model.announce_update()
            
    def update_locale(self, index):
        if index >= 0:
            locale_code = self.model.get_locale_code(index)
            self.model.set('Language', 'code', locale_code)
            self.model.announce_update()

    def load_defaults(self):
        """Load defaults."""
        self.model.read_string(self.model.defaults)
        self.model.announce_update()

    def apply_settings(self):
        """Override settings."""
        with open('config.ini', 'w', encoding='utf-8') as configfile:
           self.model.write(configfile)
