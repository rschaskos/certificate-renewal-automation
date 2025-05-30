import os
import sys
import configparser
import re

from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PySide6.QtCore import QEvent, Signal, Slot
from PySide6.QtGui import QIcon
from src.sitLogin import Ui_MainWindow
from src.sitAbout import Ui_Form
from src.sitCheckBox import Ui_CheckBox
from cryptography.fernet import Fernet
from src.utils import constructedFilePath


# --- Variáveis para persistência ---
CONFIG_FILE = 'config.ini' # Nome do arquivo de configuração
KEY_FILE = 'key.key' # Nome do arquivo da chave de criptografia
# --- Fim das variáveis para persistência ---

# --- INÍCIO DAS CLASSES AUXILIARES (MOVIDAS PARA CIMA) ---

class AboutWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class _CheckBox(QWidget, Ui_CheckBox):
    automationData = Signal(str, str, str, list) # Sinal que emite user, pass, sitNumber, selectedFiles

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushLimpar.clicked.connect(self.clearFields) # Quando clicar em Limpar
        self.pushIniciar.clicked.connect(self.validateAll) # Quando clicar em Iniciar
        self.lineEdit.returnPressed.connect(self.validateAll) # Quando enter for pressionado
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
                'Aviso',
                'Digite o número SIT.'
            )
            return False

        keywords = {
            'fgts': 'fgts',
            'estadual': 'estadual',
            'tce': 'tce',
            'trabalhista': 'trabalhista',
            'federal': 'federal',
            'municipal': 'municipal'
        }

        found_files = {}

        exec_dir = constructedFilePath('')

        try:
            if getattr(sys, 'frozen', False):
                available_files = [f for f in os.listdir(os.getcwd()) if f.lower().endswith('.pdf')]
            else:
                available_files = [f for f in os.listdir(exec_dir) if f.lower().endswith('.pdf')]

            for keyword_type, keyword_name in keywords.items():
                for file_name in available_files:
                    pattern = re.compile(r'^{}.*\.pdf$'.format(re.escape(keyword_name)), re.IGNORECASE)
                    full_file_path = constructedFilePath(file_name)

                    if pattern.match(file_name) and os.path.exists(full_file_path):
                        found_files[keyword_type] = file_name
                        break

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao listar arquivos PDF: {e}')
            return False

        missedFiles = []
        selected_keywords = []

        if self.checkBoxFgts.isChecked():
            selected_keywords.append('fgts')
        if self.checkBoxEstadual.isChecked():
            selected_keywords.append('estadual')
        if self.checkBoxTce.isChecked():
            selected_keywords.append('tce')
        if self.checkBoxTrabalhista.isChecked():
            selected_keywords.append('trabalhista')
        if self.checkBoxFederal.isChecked():
            selected_keywords.append('federal')
        if self.checkBoxMunicipal.isChecked():
            selected_keywords.append('municipal')

        if not selected_keywords:
            QMessageBox.warning(
                self,
                'Aviso',
                'Selecione pelo menos um arquivo para prosseguir.'
            )
            return False

        for keyword in selected_keywords:
            if keyword not in found_files:
                missedFiles.append(f'{keywords[keyword]}.pdf (ou variações)')

        if missedFiles:
            errorMessage = "Os seguintes tipos de arquivos selecionados não foram encontrados na pasta:\n"
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
                    [found_files[k] for k in selected_keywords]
                )
            return True

# --- FIM DAS CLASSES AUXILIARES ---

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.aboutWindow = AboutWindow()
        self.toolButton.clicked.connect(self.openAboutWindow) # Quando clicar em toolButton

        self.checkBoxWindow = _CheckBox()

        # Conectando o sinal da checkBoxWindow ao slot da MainWindow
        self.checkBoxWindow.automationData.connect(self.startAutomation)

        # --- CORREÇÃO AQUI: Conectar ao processLogin em vez de openCheckBoxWindow ---
        self.pushEntrar.clicked.connect(self.processLogin)
        self.lineCpf.returnPressed.connect(self.processLogin)
        self.linePass.returnPressed.connect(self.processLogin)
        # --- Fim da correção ---

        self.userLogin = None
        self.passLogin = None
        self.bot = None # Armazena a instância de TCEPRBot


        # --- Adições para "Lembre-me" ---
        self.config = configparser.ConfigParser()
        self.fernet_key = self._load_or_generate_key()
        self.cipher_suite = Fernet(self.fernet_key)

        self._load_credentials() # Carrega credenciais ao iniciar
        # --- Fim das adições ---

    # --- Funções de Criptografia/Descriptografia e Gerenciamento de Chave ---
    def _load_or_generate_key(self):
        key_path = constructedFilePath(KEY_FILE)
        if os.path.exists(key_path):
            with open(key_path, 'rb') as kf:
                return kf.read()
        else:
            key = Fernet.generate_key()
            try:
                with open(key_path, 'wb') as kf:
                    kf.write(key)
            except IOError as e:
                QMessageBox.critical(self, 'Erro', f'Não foi possível salvar a chave de criptografia: {e}')
            return key

    def _encrypt_data(self, data):
        return self.cipher_suite.encrypt(data.encode()).decode()

    def _decrypt_data(self, encrypted_data):
        try:
            return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            return ""

    def _save_credentials(self):
        config_path = constructedFilePath(CONFIG_FILE)

        self.config.read(config_path)

        if not self.config.has_section('Login'):
            self.config.add_section('Login')

        if self.checkBoxRememberMe.isChecked():
            self.config.set('Login', 'username', self.lineCpf.text())
            encrypted_password = self._encrypt_data(self.linePass.text())
            self.config.set('Login', 'password', encrypted_password)
            self.config.set('Login', 'remember_me', 'True')
        else:
            if self.config.has_option('Login', 'username'):
                self.config.remove_option('Login', 'username')
            if self.config.has_option('Login', 'password'):
                self.config.remove_option('Login', 'password')
            self.config.set('Login', 'remember_me', 'False')

        try:
            with open(config_path, 'w') as configfile:
                self.config.write(configfile)
        except IOError as e:
            QMessageBox.critical(self, 'Erro ao Salvar', f'Não foi possível salvar as configurações: {e}')


    def _load_credentials(self):
        config_path = constructedFilePath(CONFIG_FILE)
        if os.path.exists(config_path):
            self.config.read(config_path)
            if self.config.has_section('Login') and self.config.getboolean('Login', 'remember_me', fallback=False):
                username = self.config.get('Login', 'username', fallback='')
                encrypted_password = self.config.get('Login', 'password', fallback='')

                self.lineCpf.setText(username)

                decrypted_password = self._decrypt_data(encrypted_password)
                self.linePass.setText(decrypted_password)

                self.checkBoxRememberMe.setChecked(True)
            else:
                self.checkBoxRememberMe.setChecked(False)
        else:
            self.checkBoxRememberMe.setChecked(False)

    def _toggle_remember_me(self, state):
        pass

    # --- Fim das Funções de Criptografia/Descriptografia e Gerenciamento de Chave ---

    def openAboutWindow(self):
        self.aboutWindow.show()

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()

    def processLogin(self):
        self.userLogin = self.lineCpf.text().strip()
        self.passLogin = self.linePass.text().strip()

        cpfLen = len(self.userLogin)

        if not self.userLogin or not self.passLogin:
            QMessageBox.warning(self, 'Erro de Login', 'Por favor, insira CPF e Senha.')
            return False

        if cpfLen != 11:
            QMessageBox.warning(self, 'SIT', 'CPF inválido. O CPF deve conter 11 dígitos.')
            return False

        self._save_credentials()

        self.openCheckBoxWindow()
        return True

    def openCheckBoxWindow(self):
        self.checkBoxWindow.setMainWindow(self)
        self.checkBoxWindow.show()

    @Slot(str, str, str, list)
    def startAutomation(self, userLogin, passLogin, sitNumber, selectedFiles):
        from src.automaWeb import TCEPRBot
        if self.bot is None:
            self.bot = TCEPRBot(userLogin, passLogin, sitNumber, selectedFiles)
            self.bot.launchBrowser()
        else:
            self.bot.sitNumber = sitNumber
            self.bot.selectedFiles = selectedFiles
            self.bot._navegate()
            self.bot.certificateSelection(selectedFiles)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('favicon.ico'))
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())