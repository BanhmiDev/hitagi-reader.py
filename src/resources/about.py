# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(441, 360)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(441, 360))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setObjectName("pushButton_close")
        self.verticalLayout_2.addWidget(self.pushButton_close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">About</span></p><p><span style=\" font-size:large; font-weight:600;\">Hitagi Reader</span><br/>Hitagi Reader is an open-sourced image viewer licensed under the MIT license.<br/>Contribute via the <a href=\"https://github.com/gimu/hitagi-reader\"><span style=\" text-decoration: underline; color:#0000ff;\">official GitHub repository</span></a>.</p><p><span style=\" font-weight:600;\">PyQt5 Library</span><br/>PyQt is one of the two most popular Python bindings for the Qt cross-platform GUI/XML/<br/>SQL C++ framework (another binding is <a href=\"https://wiki.python.org/moin/PySide\"><span style=\" text-decoration: underline; color:#0000ff;\">PySide</span></a>). PyQt developed by Riverbank <br/>Computing Limited. Qt itself is developed as part of the <a href=\"http://qt-project.org\"><span style=\" text-decoration: underline; color:#0000ff;\">Qt Project</span></a>. PyQt provides <br/>bindings for Qt 4 and Qt 5. PyQt is distributed under a <a href=\"https://wiki.python.org/moin/PyQt/PyQtLicensing\"><span style=\" text-decoration: underline; color:#0000ff;\">choice of licences</span></a>: GPL <br/>version 2, GPL version 3, or a commercial license. </p><p><span style=\" font-weight:600;\">Icons</span><br/>Icons provided by the free and open-sourced project <a href=\"http://ionicons.com/\"><span style=\" text-decoration: underline; color:#0000ff;\">ionicons</span></a>.</p></body></html>"))
        self.pushButton_close.setText(_translate("Dialog", "Close"))

