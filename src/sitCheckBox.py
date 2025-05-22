# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sitCheckBox.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_CheckBox(object):
    def setupUi(self, CheckBox):
        if not CheckBox.objectName():
            CheckBox.setObjectName(u"CheckBox")
        CheckBox.resize(455, 345)
        font = QFont()
        font.setPointSize(16)
        CheckBox.setFont(font)
        self.horizontalLayout = QHBoxLayout(CheckBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBoxTce = QCheckBox(CheckBox)
        self.checkBoxTce.setObjectName(u"checkBoxTce")

        self.gridLayout.addWidget(self.checkBoxTce, 3, 0, 1, 1)

        self.checkBoxFederal = QCheckBox(CheckBox)
        self.checkBoxFederal.setObjectName(u"checkBoxFederal")

        self.gridLayout.addWidget(self.checkBoxFederal, 5, 0, 1, 1)

        self.label = QLabel(CheckBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.checkBoxMunicipal = QCheckBox(CheckBox)
        self.checkBoxMunicipal.setObjectName(u"checkBoxMunicipal")

        self.gridLayout.addWidget(self.checkBoxMunicipal, 6, 0, 1, 1)

        self.checkBoxTrabalhista = QCheckBox(CheckBox)
        self.checkBoxTrabalhista.setObjectName(u"checkBoxTrabalhista")

        self.gridLayout.addWidget(self.checkBoxTrabalhista, 4, 0, 1, 1)

        self.checkBoxFgts = QCheckBox(CheckBox)
        self.checkBoxFgts.setObjectName(u"checkBoxFgts")

        self.gridLayout.addWidget(self.checkBoxFgts, 1, 0, 1, 1)

        self.checkBoxEstadual = QCheckBox(CheckBox)
        self.checkBoxEstadual.setObjectName(u"checkBoxEstadual")

        self.gridLayout.addWidget(self.checkBoxEstadual, 2, 0, 1, 1)

        self.lineEdit = QLineEdit(CheckBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.pushLimpar = QPushButton(CheckBox)
        self.pushLimpar.setObjectName(u"pushLimpar")

        self.gridLayout.addWidget(self.pushLimpar, 7, 0, 1, 1)

        self.pushIniciar = QPushButton(CheckBox)
        self.pushIniciar.setObjectName(u"pushIniciar")

        self.gridLayout.addWidget(self.pushIniciar, 7, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.retranslateUi(CheckBox)

        QMetaObject.connectSlotsByName(CheckBox)
    # setupUi

    def retranslateUi(self, CheckBox):
        CheckBox.setWindowTitle(QCoreApplication.translate("CheckBox", u"Updater", None))
        self.checkBoxTce.setText(QCoreApplication.translate("CheckBox", u"TCE", None))
        self.checkBoxFederal.setText(QCoreApplication.translate("CheckBox", u"FEDERAL", None))
        self.label.setText(QCoreApplication.translate("CheckBox", u"N\u00ba SIT:", None))
        self.checkBoxMunicipal.setText(QCoreApplication.translate("CheckBox", u"MUNICIPAL", None))
        self.checkBoxTrabalhista.setText(QCoreApplication.translate("CheckBox", u"TRABALHISTA", None))
        self.checkBoxFgts.setText(QCoreApplication.translate("CheckBox", u"FGTS", None))
        self.checkBoxEstadual.setText(QCoreApplication.translate("CheckBox", u"ESTADUAL", None))
        self.pushLimpar.setText(QCoreApplication.translate("CheckBox", u"Limpar", None))
        self.pushIniciar.setText(QCoreApplication.translate("CheckBox", u"Iniciar", None))
    # retranslateUi

