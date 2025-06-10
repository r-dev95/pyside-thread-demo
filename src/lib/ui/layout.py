# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'layout.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDialog,
    QFrame, QGridLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(600, 500)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_stop = QPushButton(Dialog)
        self.button_stop.setObjectName(u"button_stop")

        self.gridLayout.addWidget(self.button_stop, 0, 1, 1, 1)

        self.button_start = QPushButton(Dialog)
        self.button_start.setObjectName(u"button_start")

        self.gridLayout.addWidget(self.button_start, 0, 0, 1, 1)

        self.list_widget_log = QListWidget(Dialog)
        self.list_widget_log.setObjectName(u"list_widget_log")
        self.list_widget_log.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.gridLayout.addWidget(self.list_widget_log, 3, 0, 1, 2)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.checkbox_auto_scroll = QCheckBox(self.frame)
        self.checkbox_auto_scroll.setObjectName(u"checkbox_auto_scroll")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkbox_auto_scroll.sizePolicy().hasHeightForWidth())
        self.checkbox_auto_scroll.setSizePolicy(sizePolicy1)
        self.checkbox_auto_scroll.setChecked(True)

        self.gridLayout_2.addWidget(self.checkbox_auto_scroll, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.button_stop.setText(QCoreApplication.translate("Dialog", u"Stop", None))
        self.button_start.setText(QCoreApplication.translate("Dialog", u"Start", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Log:", None))
        self.checkbox_auto_scroll.setText(QCoreApplication.translate("Dialog", u"Auto Scroll", None))
    # retranslateUi

