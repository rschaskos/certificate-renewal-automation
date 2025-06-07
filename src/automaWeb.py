from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException

from time import sleep
from src.readerPDF import ReaderPDF
from src.utils import constructedFilePath

URL = 'https://sit.tce.pr.gov.br/sitListarTransferencias.aspx'

XPATH_TIPO = '//*[@id="ContentPlaceHolder1_ddlTipoCertidao"]'
XPATH_CERTI_BOX = '//*[@id="ContentPlaceHolder1_tbNumeroCertidao"]'
XPATH_EMIT_BOX = '//*[@id="ContentPlaceHolder1_ucdtEmissao_textBoxData"]'
XPATH_VALID_BOX = '//*[@id="ContentPlaceHolder1_ucdtValidade_textBoxData"]'
XPATH_SAVE = '//*[@id="ContentPlaceHolder1_btnNovo"]'
XPATH_INIT = '//*[@id="btlInicioPrincipal"]'

XPATH_ERROR_EMIT = '//*[@id="ContentPlaceHolder1_ucdtEmissao_cvtbData"]'
XPATH_CORRECTION = '//*[@id="lsTomador_hlItem_1"]'
XPATH_ERROR_VALID = '//*[@id="ContentPlaceHolder1_ucdtValidade_cvtbData"]'

t1 = 1.5
t2 = 2
t3 = 3
t4 = 3
CERTIFICATE_TYPE_MAP = {
    'fgts': '/option[8]', 
    'municipal': '/option[2]',
    'estadual': '/option[3]',
    'tce': '/option[5]',
    'trabalhista': '/option[6]',
    'federal': '/option[9]',
}
# --- Fim das Constantes ---

class TCEPRBot:
    def __init__(self, user, passwd, sitNumber, selectedFiles, url=URL, detach=True):
        self.url = url
        self.user = user
        self.passwd = passwd
        self.sitNumber = sitNumber
        self.selectedFiles = selectedFiles
        self.detach = detach
        self.browser = None
        self._setupChromeOptions()

    def _setupChromeOptions(self):
        self.chromeOptions = Options()
        if self.detach:
            self.chromeOptions.add_experimental_option("detach", True)
        # self.chromeOptions.add_argument("--headless") # Descomente para rodar sem interface gráfica

    def launchBrowser(self):
        try:
            service = Service(ChromeDriverManager().install())
            self.browser = webdriver.Chrome(service=service, options=self.chromeOptions)
            self.browser.get(self.url)
            self.browser.maximize_window()
            self._login()
        except Exception as e:
            print(f"Erro ao iniciar o navegador ou navegar: {e}")
            # self.quit_browser() # Garante que o navegador seja fechado em caso de erro


    def _login(self):        
        try:
            self.browser.find_element(By.XPATH, '//*[@id="Login"]').send_keys(self.user)
            self.browser.find_element(By.XPATH, '//*[@id="Senha"]').send_keys(self.passwd)
            self.browser.find_element(By.XPATH, '//*[@id="btnLogin"]').click()
            sleep(t3)
            self._navegate()
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            self.quit_browser()

    def _navegate(self):
        try:
            self.browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_tbidTransferencia"]').send_keys(self.sitNumber)
            sleep(t1)
            self.browser.find_element(By.XPATH, '//*[@id="btPesquisar"]').click()
            sleep(t1)
            self.browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_gvListaTransferencias_btnDetalhes_0"]').click()
            sleep(t2)
            self.browser.find_element(By.XPATH, '//*[@id="my_menu"]/div[4]/span').click()
            sleep(t2)
            self.browser.find_element(By.XPATH, '//*[@id="lsTomador_hlItem_1"]').click()
            sleep(t1)
            self.certificateSelection(self.selectedFiles)

        except NoSuchElementException as e:
            print(f"Erro de elemento não encontrado durante a navegação/login: {e}")
            # self.quit_browser()
        except Exception as e:
            print(f"Erro inesperado durante a navegação/login: {e}")
            # self.quit_browser()

    def onErrorDate(self, browser, XPATH_ERROR, XPATH_CORRECTION):
        try:
            error_element = browser.find_element(By.XPATH, XPATH_ERROR)
            if error_element.is_displayed():
                print("Erro de data encontrado, corrigindo...")
                browser.find_element(By.XPATH, XPATH_CORRECTION).click()
                sleep(t2)
                return True
        except NoSuchElementException:
            return False
        except Exception as e:
            print(f"Erro ao verificar ou corrigir data: {e}")
            return False

    def _saveCertificate(self, readerObj, xpath_option_suffix):
        try:
            self.browser.find_element(By.XPATH, XPATH_TIPO + xpath_option_suffix).click()
            sleep(t1)

            self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).clear()
            self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerObj.certiNumber)
            sleep(t1)

            for _ in range(3):
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerObj.emitDate)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()

                if not self.onErrorDate(self.browser, XPATH_ERROR_EMIT, XPATH_CORRECTION):
                    break
                sleep(t1)
            else:
                print(f"Erro persistente na data de emissão para {readerObj.pathFile}. Pulando.")
                return False

            sleep(t1)

            for _ in range(3):
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerObj.finalValid)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()

                if not self.onErrorDate(self.browser, XPATH_ERROR_VALID, XPATH_CORRECTION):
                    break
                sleep(t1)
            else:
                print(f"Erro persistente na data de validade para {readerObj.pathFile}. Pulando.")
                return False

            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            
            try:
                alert = self.browser.switch_to.alert
                alert.accept()
                sleep(t2)
            except UnexpectedAlertPresentException:
                print(f"Nenhum alerta presente após salvar para {readerObj.pathFile}. Pode ser um erro.")
            
            return True

        except NoSuchElementException as e:
            print(f"Erro de elemento não encontrado ao preencher/salvar para {readerObj.pathFile}: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado ao preencher/salvar para {readerObj.pathFile}: {e}")
            return False

    def certificateSelection(self, selectedFiles):
        numSelected = len(selectedFiles)
        processedCount = 0

        for fileName in self.selectedFiles:
            certType = fileName.split('.')[0].lower()

            if certType not in CERTIFICATE_TYPE_MAP:
                print(f"Tipo de certificado '{certType}' do arquivo '{fileName}' não mapeado. Pulando.")
                continue

            pdfPath = constructedFilePath(fileName)
            readerObj = ReaderPDF(pdfPath)

            if readerObj.certiNumber and readerObj.emitDate and readerObj.finalValid:
                if self._saveCertificate(readerObj, CERTIFICATE_TYPE_MAP[certType]):
                    processedCount += 1
                else:
                    print(f"Falha ao preencher/salvar certificado para {fileName}. Verifique os logs acima.")
            else:
                print(f"Dados incompletos ou não encontrados para {fileName}. Pulando o preenchimento.")
            
            if processedCount == numSelected:
                try:
                    self.browser.find_element(By.XPATH, XPATH_INIT).click()
                    sleep(t2)
                    print("Todos os certificados processados. Botão 'Início' clicado.")
                except NoSuchElementException:
                    print("Botão 'Início' não encontrado ou já foi clicado. Verifique a página.")
                except Exception as e:
                    print(f"Erro ao clicar no botão 'Início': {e}")
        
        if processedCount < numSelected:
            print(f"Atenção: {numSelected - processedCount} certificados não foram processados com sucesso.")