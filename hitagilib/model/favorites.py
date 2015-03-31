#!/usr/bin/env python3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from hitagilib.model.settings import SettingsModel

class FavoritesModel(object):

    def __init__(self):
        self.settings = SettingsModel()
        self.favorites = []

        for option in self.settings.options('Favorites'):
            self.add(self.settings.get('Favorites', option))

    def add(self, path):
        if path and path not in self.favorites:
            self.favorites.append(path)

    def remove(self, path):
        if path in self.favorites:
            self.favorites.remove(path)

    def items(self):
        return self.favorites

    def check_favorites(self, directory):
        if directory in self.favorites:
            return True
        else:
            return False

    def save(self):
        self.settings.remove_section('Favorites')

        if not self.settings.has_section('Favorites'):
            self.settings.add_section('Favorites')

        for index, item in enumerate(self.items()):
            if not self.settings.has_option('Favorites', str(index)):
                self.settings.set('Favorites', str(index), str(item))

        self.settings.apply_settings()
