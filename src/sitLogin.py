# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sitLogin.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(584, 425)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setFamilies([u"Academy Engraved LET"])
        font.setPointSize(14)
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 10, 541, 341))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLogo = QLabel(self.verticalLayoutWidget)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setPixmap(QPixmap(u"src/logoSIT.png"))
        self.labelLogo.setScaledContents(True)

        self.verticalLayout.addWidget(self.labelLogo)

        self.lineCpf = QLineEdit(self.verticalLayoutWidget)
        self.lineCpf.setObjectName(u"lineCpf")
        font1 = QFont()
        font1.setFamilies([u".AppleSystemUIFont"])
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setKerning(True)
        self.lineCpf.setFont(font1)
        self.lineCpf.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.lineCpf.setMaxLength(11)
        self.lineCpf.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lineCpf)

        self.linePass = QLineEdit(self.verticalLayoutWidget)
        self.linePass.setObjectName(u"linePass")
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setKerning(True)
        self.linePass.setFont(font2)
        self.linePass.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.linePass.setEchoMode(QLineEdit.EchoMode.Password)
        self.linePass.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.linePass)

        self.pushEntrar = QPushButton(self.verticalLayoutWidget)
        self.pushEntrar.setObjectName(u"pushEntrar")
        font3 = QFont()
        font3.setPointSize(15)
        font3.setBold(False)
        self.pushEntrar.setFont(font3)
        self.pushEntrar.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(77, 123, 167);\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 16px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(60, 95, 130);\n"
"}")

        self.verticalLayout.addWidget(self.pushEntrar)

        self.toolButton = QToolButton(self.verticalLayoutWidget)
        self.toolButton.setObjectName(u"toolButton")
        font4 = QFont()
        font4.setPointSize(13)
        self.toolButton.setFont(font4)
        self.toolButton.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout.addWidget(self.toolButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 584, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SIT", None))
        self.labelLogo.setText("")
        self.lineCpf.setInputMask("")
        self.lineCpf.setPlaceholderText(QCoreApplication.translate("MainWindow", u"CPF para entrar", None))
        self.linePass.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Senha", None))
        self.pushEntrar.setText(QCoreApplication.translate("MainWindow", u"Entrar", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
    # retranslateUi

