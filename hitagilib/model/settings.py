#!/usr/bin/env python3
from configparser import ConfigParser

class SettingsModel(ConfigParser):

    def __init__(self):
        ConfigParser.__init__(self)
        self.optionxform = str
        self.read('config.ini', encoding='utf-8')
        self.defaults = """
        [Hotkeys]
        Exit = Ctrl+X
        Fullscreen = F
        Directory = D
        Next = Right
        Previous = Left
        Zoom in = Ctrl++
        Zoom out = Ctrl+-
        Zoom original = Ctrl+0
        """
        self._update_funcs = []

    def subscribe_update_func(self, func):
        """Subscribe a view method for updating."""
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    def unsubscribe_update_func(self, func):
        """Unsubscribe a view method for updating."""
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    def announce_update(self):
        """Update registered view methods."""
        for func in self._update_funcs:
            func()

    def get_locale_code(self, index):
        """Get locale code by index."""
        locale_code = ['en_US', 'de_DE', 'ja_JP', 'vi_VN']
        return locale_code[index]

    def apply_settings(self):
        """Write settings to file."""
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            self.write(configfile)
            
