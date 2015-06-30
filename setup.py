import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "includes": ['xml', 'xml.etree', 'xml.etree.ElementTree', 'logging', 'configparser', 'pathlib', 'webbrowser', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.uic'],
    "include_files": ['hitagilib/', 'resources/'] 
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "hitagi",
    version = "1.0",
    description = "An image and manga viewer",
    options = {
        "build_exe": build_exe_options
    },
    executables = [Executable("Hitagi.py", base=base)]
)
