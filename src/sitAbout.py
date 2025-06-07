# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sitAbout.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(646, 206)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelAbout = QLabel(Form)
        self.labelAbout.setObjectName(u"labelAbout")
        self.labelAbout.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelAbout)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"About", None))
        self.labelAbout.setText(QCoreApplication.translate("Form",
    u"<html><head/><body>"
    u"<p>Nome do Programa: Atualizador de Certidões</p>"
    u"<p>Versão: 2.0 </p>"
    u"<p>Descrição: Este programa foi desenvolvido para realizar tarefas repetitivas no SIT.</p>"
    u"<p>Desenvolvedor: Roney Schaskos </p>"
    u"<p>Data de Lançamento: maio de 2025</p>"
    u"<p>Tecnologias Utilizadas: Python, PySide6</p>"
    u"</body></html>", None))
    # retranslateUi

