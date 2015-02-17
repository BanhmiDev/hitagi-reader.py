#!/usr/bin/env python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from model.settings import SettingsModel

class FavoritesModel(object):

    def __init__(self):
        self.settings = SettingsModel()
        self.favorites = []

    def add(self, path):
        if path not in self.favorites:
            self.favorites.append(path)

    def remove(self, path):
        self.favorites.remove(path)

    def items(self):
        return self.favorites

    def save(self):
        if not self.settings.has_section('Favorites'):
            self.settings.add_section('Favorites')

        for index, item in enumerate(self.items()):
            if not self.settings.has_option('Favorites', str(index)):
                self.settings.set('Favorites', str(index), str(item))
                
        self.settings.apply_settings()
