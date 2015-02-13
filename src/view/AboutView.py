#!/usr/bin/env python
from PyQt5.QtWidgets import QDialog

from resources.about import Ui_Dialog

class AboutDialog(QDialog):

    def __init__(self, parent, model, controller):
        self.model = model
        self.controller = controller
        super(AboutDialog, self).__init__(parent)
        self.build_ui()

    def build_ui(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton_close.clicked.connect(self.close)
