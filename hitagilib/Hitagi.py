#!/usr/bin/env python3
import time, io, traceback, sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QMessageBox

from hitagilib.model.app import AppModel
from hitagilib.model.settings import SettingsModel
from hitagilib.controller.main import MainController
from hitagilib.view.MainView import MainView

class Hitagi(QMainWindow):
    def __init__(self):
        super(Hitagi, self).__init__()
        self.model = AppModel()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()

def excepthook(exception_type, exception_value, traceback_obj):
    """Global function to catch unhandled exceptions."""
    separator = '-' * 80
    notice = \
        """An unhandled exception occurred. Please report this error using\n"""\
        """GitHub Issues <https://github.com/gimu/hitagi-reader/issues>."""\
        """\n\nException saved in error.log"""\
        """\n\nError information:\n"""
    time_string = time.strftime("%Y-%m-%d, %H:%M:%S")
    tbinfofile = io.StringIO()
    traceback.print_tb(traceback_obj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()

    # Create error message
    error_msg = '%s: \n%s' % (str(exception_type), str(exception_value))
    sections = [separator, time_string, separator, error_msg, separator, tbinfo]

    # Combine and write to file
    msg = '\n'.join(sections)
    try:
        f = open('error.log', 'w')
        f.write(msg)
        f.close()
    except IOError:
        pass

    # GUI message
    error_box = QMessageBox()
    error_box.setWindowTitle('Error occured')
    error_box.setText(str(notice) + str(msg))
    error_box.exec_()

def run():
    # Global exceptions
    sys.excepthook = excepthook

    app = QApplication(sys.argv) 

    # Splash screen
    splash_pix = QPixmap('resources/splash.jpg')
    splash = QSplashScreen(splash_pix)
    splash.setMask(splash_pix.mask())
    splash.show()
    
    app.processEvents()
    
    # Load translation
    locale_code = SettingsModel().get('Language', 'code')
    if locale_code != "en_US": # Standard language
        # Standard translator for the generated GUI
        translator = QTranslator()
        translator.load('localization/' + locale_code + '.qm')
        app.installTranslator(translator)

        # Translator for various GUI elements
        translator_2 = QTranslator()
        translator_2.load('localization/' + locale_code + '_2.qm')
        app.installTranslator(translator_2)

    # Start
    m = Hitagi()
    
    splash.finish(m)
    sys.exit(app.exec())
