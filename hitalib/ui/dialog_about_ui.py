# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Sat Oct 18 17:09:39 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.setWindowModality(QtCore.Qt.WindowModal)
        About.resize(400, 300)
        self.label = QtGui.QLabel(About)
        self.label.setGeometry(QtCore.QRect(90, 90, 271, 111))
        self.label.setObjectName("label")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        About.setWindowTitle(QtGui.QApplication.translate("About", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("About", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Hitagi Reader 1.0</span></p><p><a href=\"http://github.com/gimu/hitagi-reader\"><span style=\" text-decoration: underline; color:#0000ff;\">http://github.com/gimu/hitagi-reader</span></a></p><p>Hitagi Reader is licensed under the <a href=\"http://www.apache.org/licenses/LICENSE-2.0.html\"><span style=\" text-decoration: underline; color:#0000ff;\">Apache 2.0</span></a> License.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

