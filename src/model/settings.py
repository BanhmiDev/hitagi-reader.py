#!/usr/bin/env python
from configparser import ConfigParser

from PyQt5 import QtGui, QtWidgets

class SettingsModel(ConfigParser):

    def __init__(self):
        ConfigParser.__init__(self)
        self.optionxform = str
        self.read('config.ini', encoding='utf-8')

        self._update_funcs = []

        self.applied = False

    # subscribe a view method for updating
    def subscribe_update_func(self, func):
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    # unsubscribe a view method for updating
    def unsubscribe_update_func(self, func):
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    # update registered view methods
    def announce_update(self):
        for func in self._update_funcs:
            func()
    
    def apply_settings(self):
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            self.write(configfile)
            