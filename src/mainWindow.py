import os
import sys
import configparser
import re

from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QCheckBox, QLabel, QVBoxLayout
from PySide6.QtCore import QEvent, Signal, Slot, QThread, QTimer, Qt, QObject
from PySide6.QtGui import QIcon, QScreen # QScreen é importado mas não usado, pode ser removido

from src.sitLogin import Ui_MainWindow
from src.sitAbout import Ui_Form
from src.sitCheckBox import Ui_CheckBox
from cryptography.fernet import Fernet
from src.utils import constructedFilePath
from src.automaWeb import TCEPRBot

# --- Variáveis de Configuração ---
CONFIG_FILE = 'config.ini'
KEY_FILE = 'key.key'
# --- Fim das Variáveis de Configuração ---

# --- Classe: TemporaryMessageWindow ---
class TemporaryMessageWindow(QWidget):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.SplashScreen |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        layout = QVBoxLayout(self)
        label = QLabel(message, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px; padding: 20px; background-color: #333; color: white; border-radius: 10px;")
        layout.addWidget(label)
        self.setLayout(layout)

        self.adjustSize()
        self.centerOnScreen()

    def centerOnScreen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def show_and_auto_close(self, duration_ms):
        self.show()
        QTimer.singleShot(duration_ms, self.close)

# --- Classe: AutomationWorker ---
class AutomationWorker(QObject):
    finished = Signal()
    error = Signal(str)

    def __init__(self, bot_instance, userLogin, passLogin, sitNumber, selectedFiles, parent=None):
        super().__init__(parent)
        self.bot = bot_instance
        self.userLogin = userLogin
        self.passLogin = passLogin
        self.sitNumber = sitNumber
        self.selectedFiles = selectedFiles

    @Slot()
    def run(self):
        try:
            # Garante que a instância do bot tem os dados mais recentes para esta automação.
            self.bot.user = self.userLogin
            self.bot.passwd = self.passLogin
            self.bot.sitNumber = self.sitNumber
            self.bot.selectedFiles = self.selectedFiles

            if self.bot.browser is None:
                # Primeira automação: Lança navegador e faz login
                self.bot.launchBrowser()
            else:
                # Automações subsequentes: navegador já está aberto e logado.
                # Reutiliza o navegador e executa a navegação e preenchimento para o novo SIT.
                self.bot._navegate()

            self.finished.emit()
        except Exception as e:
            # Captura erros da automação e os envia para a thread principal
            self.error.emit(f"Erro na automação: {e}")
            self.finished.emit()

# --- Classe: AboutWindow ---
class AboutWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

# --- Classe: _CheckBox (Renomeada para CheckBoxWindow para melhor clareza) ---
class CheckBoxWindow(QWidget, Ui_CheckBox): # Alterado de _CheckBox para CheckBoxWindow
    closed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushLimpar.clicked.connect(self.clearFields)
        self.pushIniciar.clicked.connect(self.validateAll)
        self.lineEdit.returnPressed.connect(self.validateAll)
        self.mainWindow = None # Será definida pela MainWindow

        self.checkbox_map = {
            self.checkBoxFgts: 'fgts.pdf',
            self.checkBoxMunicipal: 'municipal.pdf',
            self.checkBoxEstadual: 'estadual.pdf',
            self.checkBoxTce: 'tce.pdf',
            self.checkBoxTrabalhista: 'trabalhista.pdf',
            self.checkBoxFederal: 'federal.pdf'
        }

    def setMainWindow(self, main_window):
        self.mainWindow = main_window

    def clearFields(self):
        self.lineEdit.clear()
        for checkbox in self.checkbox_map.keys():
            checkbox.setChecked(False)

    def validateAll(self):
        sitNumber = self.lineEdit.text().strip()
        selectedFiles = []
        missedFiles = []
        found_all_selected = True

        if not sitNumber:
            QMessageBox.warning(self, 'Erro', 'O campo "Nº SIT" não pode estar vazio.')
            return

        for checkbox, file_name in self.checkbox_map.items():
            if checkbox.isChecked():
                selectedFiles.append(file_name)
                file_path = constructedFilePath(file_name)
                if not os.path.exists(file_path):
                    missedFiles.append(file_name)
                    found_all_selected = False

        if not selectedFiles:
            QMessageBox.warning(self, 'Erro', 'Nenhum certificado selecionado. Por favor, marque ao menos um.')
            return

        if not found_all_selected:
            msg = "Os seguintes arquivos não foram encontrados:\n" + "\n".join(missedFiles) + "\n\nPor favor, verifique se eles estão na pasta correta."
            QMessageBox.critical(self, 'Arquivos Ausentes', msg)
            return

        self.hide() # Esconde a janela de seleção enquanto a automação roda

        # Mostra a mensagem temporária de "Iniciando automação"
        self.temp_msg_window = TemporaryMessageWindow("Iniciando automação, por favor, aguarde...", self.mainWindow)
        self.temp_msg_window.show_and_auto_close(3000) # Exibe por 3 segundos

        # Prepara e inicia a automação em uma nova thread
        self.thread = QThread()

        # Garante que a instância do bot existe na MainWindow. Se ainda não existe, cria.
        # Isso é crucial para persistir a instância do browser.
        if self.mainWindow.bot is None:
            # Inicializa o bot com dados vazios, pois eles serão atualizados pelo worker antes da execução.
            self.mainWindow.bot = TCEPRBot(
                self.mainWindow.userLogin,
                self.mainWindow.passLogin,
                "", # sitNumber inicial vazio
                []  # selectedFiles inicial vazio
            )

        # Cria o worker, passando a instância do bot e os dados da automação
        self.worker = AutomationWorker(
            self.mainWindow.bot,
            self.mainWindow.userLogin,
            self.mainWindow.passLogin,
            sitNumber, # SIT Number atual para esta execução
            selectedFiles # Arquivos selecionados para esta execução
        )
        self.worker.moveToThread(self.thread)

        # Conecta os sinais e slots para gerenciar a thread
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.error.connect(self.handleAutomationError)
        # Reexibe a janela de seleção após a thread terminar (sucesso ou erro)
        self.thread.finished.connect(self.show)

        self.thread.start() # Inicia a thread

    @Slot(str)
    def handleAutomationError(self, error_message):
        QMessageBox.critical(self, 'Erro na Automação', error_message)

    def closeEvent(self, event):
        # Emite um sinal para a MainWindow saber que esta janela foi fechada
        self.closed.emit()
        event.accept()

# --- Classe Principal: MainWindow ---
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('SIT - Automação')
        
        self.cipher_suite = None
        self._load_or_generate_key()

        self.userLogin = ''
        self.passLogin = ''
        self.bot = None # Instância do TCEPRBot será criada aqui ou no CheckBoxWindow

        # Instanciação das janelas auxiliares
        self.aboutWindow = AboutWindow()
        # Usa o nome de classe ajustado
        self.checkBoxWindow = CheckBoxWindow()
        self.checkBoxWindow.setMainWindow(self)
        self.checkBoxWindow.closed.connect(self.show) # Conecta o fechamento da CheckBoxWindow para mostrar a MainWindow

        try:
            self.pushEntrar.clicked.connect(self.processLogin)
        except AttributeError:
            QMessageBox.critical(self, 'Erro de Configuração da UI',
                                 "Não foi possível encontrar o botão de login 'pushEntrar'. "
                                 "Verifique o nome do objeto no seu arquivo sitLogin.ui.")
            sys.exit(1)

        # Verifica se o checkbox 'Lembrar' existe na UI
        if not hasattr(self, 'checkBoxRememberMe'):
            print("Aviso: 'checkBoxRememberMe' (checkbox 'Lembre-me') não encontrado na UI. A funcionalidade de lembrar credenciais pode não funcionar.")

        # Verifica se o botão 'Sobre' existe na UI
        if hasattr(self, 'toolButton'):
            self.toolButton.setText('Sobre')
            self.toolButton.clicked.connect(self.showAbout)
        else:
            print("Aviso: 'toolButton' não encontrado na UI. O botão 'Sobre' não estará funcional.")

        # Carrega credenciais ao iniciar a aplicação
        self._load_credentials()

    def _load_or_generate_key(self):
        key_path = constructedFilePath(KEY_FILE)
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
        self.cipher_suite = Fernet(key)

    def _save_credentials(self, remember_me_checked):
        config_path = constructedFilePath(CONFIG_FILE)
        config = configparser.ConfigParser()

        if os.path.exists(config_path):
            config.read(config_path)

        if 'Credentials' not in config:
            config['Credentials'] = {}

        if remember_me_checked:
            encrypted_user = self.cipher_suite.encrypt(self.userLogin.encode()).decode()
            encrypted_pass = self.cipher_suite.encrypt(self.passLogin.encode()).decode()

            config['Credentials']['username'] = encrypted_user
            config['Credentials']['password'] = encrypted_pass
            config['Credentials']['remember_me'] = 'True'
        else:
            # Se 'Lembre-me' não estiver marcado ou foi desmarcado, limpe as credenciais
            if 'Credentials' in config:
                del config['Credentials']

        with open(config_path, 'w') as configfile:
            config.write(configfile)

    def _load_credentials(self):
        config_path = constructedFilePath(CONFIG_FILE)
        config = configparser.ConfigParser()
        if os.path.exists(config_path):
            config.read(config_path)
            if 'Credentials' in config:
                try:
                    encrypted_user = config['Credentials'].get('username')
                    encrypted_pass = config['Credentials'].get('password')
                    remember_me_state = config['Credentials'].get('remember_me', 'False')

                    if encrypted_user:
                        self.userLogin = self.cipher_suite.decrypt(encrypted_user.encode()).decode()
                        self.lineCpf.setText(self.userLogin)
                    if encrypted_pass:
                        self.passLogin = self.cipher_suite.decrypt(encrypted_pass.encode()).decode()
                        self.linePass.setText(self.passLogin)

                    if self.userLogin and self.passLogin and remember_me_state == 'True' and hasattr(self, 'checkBoxRememberMe'):
                        self.checkBoxRememberMe.setChecked(True)
                    elif hasattr(self, 'checkBoxRememberMe'):
                        self.checkBoxRememberMe.setChecked(False)

                except Exception as e:
                    QMessageBox.warning(self, 'Erro de Criptografia', f'Não foi possível descriptografar as credenciais salvas. Erro: {e}. As credenciais foram limpas.')
                    self.lineCpf.clear()
                    self.linePass.clear()
                    if hasattr(self, 'checkBoxRememberMe'):
                        self.checkBoxRememberMe.setChecked(False)
                    if os.path.exists(config_path):
                        os.remove(config_path)
            else:
                if hasattr(self, 'checkBoxRememberMe'):
                    self.checkBoxRememberMe.setChecked(False)

    def showAbout(self):
        self.aboutWindow.show()

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()

    def processLogin(self):
        self.userLogin = self.lineCpf.text().strip()
        self.passLogin = self.linePass.text().strip()

        if not self.userLogin or not self.passLogin:
            QMessageBox.warning(self, 'Erro de Login', 'Por favor, insira CPF e Senha.')
            return False

        if not re.fullmatch(r'\d{11}', self.userLogin):
            QMessageBox.warning(self, 'SIT', 'CPF inválido. O CPF deve conter exatamente 11 dígitos numéricos.')
            return False

        remember_me = False
        if hasattr(self, 'checkBoxRememberMe') and isinstance(self.checkBoxRememberMe, QCheckBox):
            remember_me = self.checkBoxRememberMe.isChecked()

        self._save_credentials(remember_me)

        self.openCheckBoxWindow()
        return True

    def openCheckBoxWindow(self):
        self.checkBoxWindow.show()
        self.hide()

    # O método startAutomation na MainWindow NÃO é mais necessário
    # pois a automação é iniciada diretamente do _CheckBox.validateAll()
    # via QThread, usando a instância do bot gerenciada pela MainWindow.
    # Removido:
    # @Slot(str, str, str, list)
    # def startAutomation(self, userLogin, passLogin, sitNumber, selectedFiles):
    #     # ... lógica anterior ...

    def closeEvent(self, event):
        # Garante que o navegador Selenium seja fechado ao fechar a aplicação
        if self.bot and self.bot.browser: # Verifica se o bot e o browser existem
            self.bot.quit_browser() # Assumindo que TCEPRBot.quit_browser() existe
        super().closeEvent(event)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
