# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wallpaper.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 220)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_cancel = QtWidgets.QPushButton(Dialog)
        self.button_cancel.setObjectName("button_cancel")
        self.gridLayout_2.addWidget(self.button_cancel, 1, 1, 1, 1)
        self.button_set_as_wallpaper = QtWidgets.QPushButton(Dialog)
        self.button_set_as_wallpaper.setObjectName("button_set_as_wallpaper")
        self.gridLayout_2.addWidget(self.button_set_as_wallpaper, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.radio_fit_to_width = QtWidgets.QRadioButton(self.groupBox)
        self.radio_fit_to_width.setObjectName("radio_fit_to_width")
        self.gridLayout.addWidget(self.radio_fit_to_width, 2, 0, 1, 1)
        self.radio_original_size = QtWidgets.QRadioButton(self.groupBox)
        self.radio_original_size.setChecked(True)
        self.radio_original_size.setObjectName("radio_original_size")
        self.gridLayout.addWidget(self.radio_original_size, 0, 0, 1, 1)
        self.radio_tiled = QtWidgets.QRadioButton(self.groupBox)
        self.radio_tiled.setObjectName("radio_tiled")
        self.gridLayout.addWidget(self.radio_tiled, 1, 0, 1, 1)
        self.radio_fit_to_height = QtWidgets.QRadioButton(self.groupBox)
        self.radio_fit_to_height.setObjectName("radio_fit_to_height")
        self.gridLayout.addWidget(self.radio_fit_to_height, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Set as wallpaper"))
        self.button_cancel.setText(_translate("Dialog", "Cancel"))
        self.button_set_as_wallpaper.setText(_translate("Dialog", "Set as wallpaper"))
        self.groupBox.setTitle(_translate("Dialog", "Options"))
        self.radio_fit_to_width.setText(_translate("Dialog", "Fit image to desktop width"))
        self.radio_original_size.setText(_translate("Dialog", "Use image in original size"))
        self.radio_tiled.setText(_translate("Dialog", "Tile image according to desktop"))
        self.radio_fit_to_height.setText(_translate("Dialog", "Fit image to desktop height"))

