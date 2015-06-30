#!/usr/bin/env python3
from configparser import ConfigParser

class SettingsModel(ConfigParser):

    def __init__(self):
        ConfigParser.__init__(self, allow_no_value = True)
        self.optionxform = str
        self.read('config.ini', encoding='utf-8')
        self.check()

        self.defaults = """
        [Hotkeys]
        Exit = Ctrl+X
        Fullscreen = F
        Next = Right
        Previous = Left
        Directory = D
        Slideshow = F3
        Zoom in = Ctrl++
        Zoom out = Ctrl+-
        Zoom original = Ctrl+0
        """
        
        self.locale_code = ['en_US', 'de_DE', 'ja_JP', 'vi_VN']
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

    def check(self):
        """Automatically fix a corrupt config file."""
        self.set('', ';Do not manually edit this file while it is running.')
        self.set('', ';Changes will not save until then!')
        # Check for missing sections
        if not self.has_section('Directory'):
            self.add_section('Directory')

        if not self.has_section('Hotkeys'):
            self.add_section('Hotkeys')

        if not self.has_section('Language'):
            self.add_section('Language')

        if not self.has_section('Look'):
            self.add_section('Look')

        if not self.has_section('Misc'):
            self.add_section('Misc')

        if not self.has_section('Slideshow'):
            self.add_section('Slideshow')

        if not self.has_section('Viewport'):
            self.add_section('Viewport')

        if not self.has_section('Favorites'):
            self.add_section('Favorites')

        # Add missing options (with default keybindings)
        if not self.has_option('Directory', 'default'):
            self.set('Directory', 'default', '/')

        if not self.has_option('Hotkeys', 'Exit'):
            self.set('Hotkeys', 'Exit', 'Ctrl+X')
        if not self.has_option('Hotkeys', 'Fullscreen'):
            self.set('Hotkeys', 'Fullscreen', 'F')
        if not self.has_option('Hotkeys', 'Directory'):
            self.set('Hotkeys', 'Directory', 'D')
        if not self.has_option('Hotkeys', 'Next'):
            self.set('Hotkeys', 'Next', 'Right')
        if not self.has_option('Hotkeys', 'Previous'):
            self.set('Hotkeys', 'Previous', 'Left')
        if not self.has_option('Hotkeys', 'Zoom in'):
            self.set('Hotkeys', 'Zoom in', 'Ctrl++')
        if not self.has_option('Hotkeys', 'Zoom out'):
            self.set('Hotkeys', 'Zoom out', 'Ctrl--')
        if not self.has_option('Hotkeys', 'Zoom original'):
            self.set('Hotkeys', 'Zoom original', 'Ctrl+0')
        if not self.has_option('Hotkeys', 'Rotate clockwise'):
            self.set('Hotkeys', 'Rotate clockwise', '')
        if not self.has_option('Hotkeys', 'Rotate counterclockwise'):
            self.set('Hotkeys', 'Rotate counterclockwise', '')

        if not self.has_option('Hotkeys', 'Flip horizontal'):
            self.set('Hotkeys', 'Flip horizontal', '')
        if not self.has_option('Hotkeys', 'Flip vertical'):
            self.set('Hotkeys', 'Flip vertical', '')
        if not self.has_option('Hotkeys', 'Fit to width'):
            self.set('Hotkeys', 'Fit to width', '')
        if not self.has_option('Hotkeys', 'Fit to height'):
            self.set('Hotkeys', 'Fit to height', '')
        if not self.has_option('Hotkeys', 'Add to favorites'):
            self.set('Hotkeys', 'Add to favorites', '')
        if not self.has_option('Hotkeys', 'Remove from favorites'):
            self.set('Hotkeys', 'Remove from favorites', '')
        if not self.has_option('Hotkeys', 'Slideshow'):
            self.set('Hotkeys', 'Slideshow', 'F3')

        if not self.has_option('Language', 'code'):
            self.set('Language', 'code', 'en_US')

        if not self.has_option('Look', 'background'):
            self.set('Look', 'background', '#3d3636')

        if not self.has_option('Misc', 'check_updates'):
            self.set('Misc', 'check_updates', 'True')
        if not self.has_option('Misc', 'hide_menubar'):
            self.set('Misc', 'hide_menubar', 'False')
        if not self.has_option('Misc', 'fullscreen_mode'):
            self.set('Misc', 'fullscreen_mode', 'False')

        if not self.has_option('Slideshow', 'speed'):
            self.set('Slideshow', 'speed', '1')
        if not self.has_option('Slideshow', 'restart'):
            self.set('Slideshow', 'restart', 'True')
        if not self.has_option('Slideshow', 'random'):
            self.set('Slideshow', 'random', 'False')
        if not self.has_option('Slideshow', 'reverse'):
            self.set('Slideshow', 'reverse', 'False')

        if not self.has_option('Viewport', 'selection'):
            self.set('Viewport', 'selection', '0')

        self.apply_settings()
        
    def get_locale_code(self, index):
        """Get locale code by index."""
        return self.locale_code[index]

    def get_locale_code_index(self, code):
        return self.locale_code.index(code)

    def apply_settings(self):
        """Write settings to file."""
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            self.write(configfile)
            
