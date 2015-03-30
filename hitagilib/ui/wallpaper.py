# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wallpaper.ui'
#
# Created: Sun Feb 15 21:58:45 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_cancel = QtWidgets.QPushButton(Dialog)
        self.button_cancel.setObjectName("button_cancel")
        self.gridLayout_2.addWidget(self.button_cancel, 2, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.radio_fit_to_width = QtWidgets.QRadioButton(self.groupBox)
        self.radio_fit_to_width.setObjectName("radio_fit_to_width")
        self.gridLayout.addWidget(self.radio_fit_to_width, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setAutoFillBackground(True)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 1)
        self.radio_original_size = QtWidgets.QRadioButton(self.groupBox)
        self.radio_original_size.setObjectName("radio_original_size")
        self.gridLayout.addWidget(self.radio_original_size, 1, 0, 1, 1)
        self.radio_tiled = QtWidgets.QRadioButton(self.groupBox)
        self.radio_tiled.setObjectName("radio_tiled")
        self.gridLayout.addWidget(self.radio_tiled, 2, 0, 1, 1)
        self.radio_fit_to_height = QtWidgets.QRadioButton(self.groupBox)
        self.radio_fit_to_height.setObjectName("radio_fit_to_height")
        self.gridLayout.addWidget(self.radio_fit_to_height, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 2)
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.graphicsView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 0, 0, 1, 2)
        self.button_set_as_wallpaper = QtWidgets.QPushButton(Dialog)
        self.button_set_as_wallpaper.setObjectName("button_set_as_wallpaper")
        self.gridLayout_2.addWidget(self.button_set_as_wallpaper, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Set as wallpaper"))
        self.button_cancel.setText(_translate("Dialog", "Cancel"))
        self.groupBox.setTitle(_translate("Dialog", "Options"))
        self.radio_fit_to_width.setText(_translate("Dialog", "Fit to width"))
        self.label.setText(_translate("Dialog", "Background color"))
        self.radio_original_size.setText(_translate("Dialog", "Original size"))
        self.radio_tiled.setText(_translate("Dialog", "Tiled"))
        self.radio_fit_to_height.setText(_translate("Dialog", "Fit to height"))
        self.button_set_as_wallpaper.setText(_translate("Dialog", "Set as wallpaper"))

