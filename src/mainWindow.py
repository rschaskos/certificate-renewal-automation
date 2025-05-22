import os
import sys

from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PySide6.QtCore import QEvent, Signal, Slot
from PySide6.QtGui import QIcon
from src.sitLogin import Ui_MainWindow
from src.sitAbout import Ui_Form
from src.sitCheckBox import Ui_CheckBox


# current = Path(__file__).parent
# os.chdir(current)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.setWindowIcon(QIcon('src/favicon.ico'))

        self.aboutWindow = AboutWindow()
        self.toolButton.clicked.connect(self.openAboutWindow) # Quando clicar em toolButton

        self.checkBoxWindow = _CheckBox()

        # Conectando o sinal da checkBoxWindow ao slot da MainWindow
        self.checkBoxWindow.automationData.connect(self.startAutomation)

        self.pushEntrar.clicked.connect(self.openCheckBoxWindow) # Quando clicar em Entrar
        self.lineCpf.returnPressed.connect(self.openCheckBoxWindow) # Quando pressionar enter
        self.linePass.returnPressed.connect(self.openCheckBoxWindow) # Quando pressionar enter

        self.userLogin = None
        self.passLogin = None 
        self.bot = None # Armazena a instância de TCEPRBot

    def openAboutWindow(self):
        self.aboutWindow.show()

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()

    def openCheckBoxWindow(self):
        self.userLogin = self.lineCpf.text()
        self.passLogin = self.linePass.text()
        cpfLen = len(self.lineCpf.text())

        if cpfLen == 11:

            if self.userLogin and self.passLogin:
                # Passando a referência da MainWindow para a checkBoxWindow
                self.checkBoxWindow.setMainWindow(self)
                # print(f"MainWindow - userLogin: {self.userLogin}, passLogin: {self.passLogin}")
                self.checkBoxWindow.show()
            else:
                QMessageBox.warning(
                    self,
                    'Campo vazio',
                    'Insira a senha antes de prossegir'
                )
        else:
            QMessageBox.warning(
                    self,
                    'Campo vazio',
                    'CPF inválido'
                )

    @Slot(str, str, str, list)
    def startAutomation(self, userLogin, passLogin, sitNumber, selectedFiles):
        #*** Aqui você instanciará e chamará a sua classe TCEPRBot ***
        from src.automaWeb import TCEPRBot
        if self.bot is None:
            self.bot = TCEPRBot(userLogin, passLogin, sitNumber, selectedFiles)
            self.bot.launchBrowser()
        else:
            self.bot.sitNumber = sitNumber
            self.bot.selectedFiles = selectedFiles
            self.bot._navegate()
            self.bot.certificateSelection(selectedFiles)            

class AboutWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.setWindowIcon(QIcon('src/favicon.ico'))

class _CheckBox(QWidget, Ui_CheckBox):
    automationData = Signal(str, str, str, list) # Sinal que emite user, pass, sitNumber, selectedFiles

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.setWindowIcon(QIcon('src/favicon.ico'))

        self.pushLimpar.clicked.connect(self.clearFields) # Quando clicar em Limpar
        self.pushIniciar.clicked.connect(self.validateAll) # Quando clicar em Iniciar
        self.mainWindow = None

    def setMainWindow(self, main_window):
        self.mainWindow = main_window

    # Método que limpa o checkbox e lineEdit
    def clearFields(self):
        self.checkBoxFgts.setChecked(False)
        self.checkBoxEstadual.setChecked(False)   
        self.checkBoxTce.setChecked(False)   
        self.checkBoxTrabalhista.setChecked(False)   
        self.checkBoxFederal.setChecked(False)   
        self.checkBoxMunicipal.setChecked(False)

        self.lineEdit.clear()

    # Quando a janela checkbox for fechada
    def closeEvent(self, event):
        self.clearFields()
        event.accept()
    
    def validateAll(self):
        sitNumber = self.lineEdit.text().strip()

        if not sitNumber:
            QMessageBox.warning(
                self,
                'Campo vazio',
                'Digite o número SIT.'
            )
            return False

        checkedFiles = {}
        if self.checkBoxFgts.isChecked():
            checkedFiles['fgts.pdf'] = self.checkBoxFgts
        if self.checkBoxEstadual.isChecked():
            checkedFiles['estadual.pdf'] = self.checkBoxEstadual
        if self.checkBoxTce.isChecked():
            checkedFiles['tce.pdf'] = self.checkBoxTce
        if self.checkBoxTrabalhista.isChecked():
            checkedFiles['trabalhista.pdf'] = self.checkBoxTrabalhista
        if self.checkBoxFederal.isChecked():
            checkedFiles['federal.pdf'] = self.checkBoxFederal
        if self.checkBoxMunicipal.isChecked():
            checkedFiles['municipal.pdf'] = self.checkBoxMunicipal

        # Nova verificação: se nenhum checkbox estiver marcado
        if not checkedFiles:
            QMessageBox.warning(
                self,
                '',
                'Selecione pelo menos um arquivo para prosseguir.'
            )
            return False
        
        # print(f"Diretório de trabalho atual (validateAll): {os.getcwd()}") # ADICIONE ESTA LINHA

        missedFiles = []
        # from src.utils import constructedFilePath

        for fileName, checkbox in checkedFiles.items():
            # filePath = constructedFilePath(fileName)
            # if not os.path.exists(filePath):
            if not os.path.exists(fileName):
                missedFiles.append(fileName)

        if missedFiles:
            errorMessage = "Arquivos não encontrados na pasta:\n"
            for file in missedFiles:
                errorMessage += f'- {file}\n'
            QMessageBox.critical(self, 'Erro de arquivo', errorMessage)
            return False
        else:
            if self.mainWindow:
                self.automationData.emit(
                    self.mainWindow.userLogin,
                    self.mainWindow.passLogin,
                    sitNumber,
                    list(checkedFiles.keys())
                )
                # print(f'_CheckBox - mainWindow encontrado: {self.mainWindow}')
                # print(f'_CheckBox - mainWindow.userLogin: {self.mainWindow.userLogin},mainWindow.passLogin: {self.mainWindow.passLogin}, sitNumber: {sitNumber}')
                # print(f'_CheckBox - checkedFiles: {checkedFiles.keys()}')
            return True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('favicon.ico'))
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


