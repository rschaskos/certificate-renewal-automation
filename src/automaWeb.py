from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime


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

MESES = {'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5,
'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9,
'outubro': 10, 'novembro': 11, 'dezembro': 12}

t1 = 1
t2 = 1.5
t3 = 2
t4 = 3
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

        prefs = {
        "profile.default_content_setting_values.autofill": 2,
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False
        }

        self.chromeOptions.add_experimental_option("prefs", prefs)    

        if self.detach:
            self.chromeOptions.add_experimental_option('detach', True)

    def launchBrowser(self):

        if self.browser is None:
            try:
                serv = Service(ChromeDriverManager().install())
                self.browser = webdriver.Chrome(service=serv, options=self.chromeOptions)
                self.browser.get(self.url)
                self.browser.maximize_window()
                sleep(t1)
                self._login()
            except Exception as e:
                print(f"Erro ao iniciar o navegador: {e}")
                if self.browser:
                    self.browser.quit()
        else:
            print('Navegador já aberto...')

    def _login(self):        
        try:
            self.browser.find_element(By.XPATH, '//*[@id="Login"]').send_keys(self.user)
            sleep(t1)
            self.browser.find_element(By.XPATH, '//*[@id="Senha"]').send_keys(self.passwd)
            sleep(t1)
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
            
        except Exception as e:
            print(f'Elemento não encontrado: {e}')
            # self.quit_browser()

    def onErrorDate(self, browser, xpathError, xpathCorrection):
        try:
            erroEmit = browser.find_element(By.XPATH, xpathError)
            if erroEmit.is_displayed():
                browser.find_element(By.XPATH, xpathCorrection).click()
                sleep(t4)
                return True
        except NoSuchElementException:
            return False
        return False

    def certificateSelection(self, selectedFiles):
        numSelected = len(selectedFiles)
        processedCount = 0
        XPATH_ERROR_EMIT = '//*[@id="ContentPlaceHolder1_ucdtEmissao_cvtbData"]'
        XPATH_CORRECTION = '//*[@id="lsTomador_hlItem_1"]'
        XPATH_ERROR_VALID = '//*[@id="ContentPlaceHolder1_ucdtValidade_cvtbData"]'

        if 'fgts.pdf' in selectedFiles:
            pdfPathFgts = constructedFilePath('fgts.pdf')
            readerFGTS = ReaderPDF(pdfPathFgts)
            for c in range(3):
                self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[8]').click()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).clear()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerFGTS.certiNumberFGTS)
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerFGTS.emitDateFGTS)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                sleep(t1)

                if self.onErrorDate(self.browser, XPATH_ERROR_EMIT, XPATH_CORRECTION):
                    continue

                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerFGTS.finalValidFGTS)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                sleep(t1)

                if not self.onErrorDate(self.browser, XPATH_ERROR_VALID, XPATH_CORRECTION):
                    break

            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t2)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        if 'estadual.pdf' in selectedFiles:
            pdfPathEstadual = constructedFilePath('estadual.pdf')
            readerESTADUAL = ReaderPDF(pdfPathEstadual)
            for c in range(3):
                self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[3]').click()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).clear()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerESTADUAL.certiNumberESTADUAL)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                sleep(t1)
                
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerESTADUAL.emitDateESTADUAL)
                sleep(t1)

                if self.onErrorDate(self.browser, XPATH_ERROR_EMIT, XPATH_CORRECTION):
                    continue

                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerESTADUAL.finalValidESTADUAL)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                sleep(t1)

                if not self.onErrorDate(self.browser, XPATH_ERROR_VALID, XPATH_CORRECTION):
                    break

            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        
        if 'tce.pdf' in selectedFiles:
            pdfPathTce = constructedFilePath('tce.pdf')
            readerTCE = ReaderPDF(pdfPathTce)
            for c in range(3):
                self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[5]').click()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).clear()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerTCE.certiNumberTCE)
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerTCE.emitDateTCE)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                sleep(t1)

                if self.onErrorDate(self.browser, XPATH_ERROR_EMIT, XPATH_CORRECTION):
                    continue
                
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerTCE.finalValidTCE)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                sleep(t1)

                if not self.onErrorDate(self.browser, XPATH_ERROR_VALID, XPATH_CORRECTION):
                    break

            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        if 'trabalhista.pdf' in selectedFiles:
            pdfPathTrabalhista = constructedFilePath('trabalhista.pdf')
            readerTRABALHISTA = ReaderPDF(pdfPathTrabalhista)
            for c in range(3):
                self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[6]').click()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).clear()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerTRABALHISTA.certiNumberTRABALHISTA)
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerTRABALHISTA.emitDateTRABALHISTA)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                sleep(t1)

                if self.onErrorDate(self.browser, XPATH_ERROR_EMIT, XPATH_CORRECTION):
                    continue
                
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerTRABALHISTA.finalValidTRABALHISTA)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                sleep(t1)

                if not self.onErrorDate(self.browser, XPATH_ERROR_VALID, XPATH_CORRECTION):
                    break

            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        
        if 'federal.pdf' in selectedFiles:
            pdfPathFederal = constructedFilePath('federal.pdf')
            readerFEDERAL = ReaderPDF(pdfPathFederal)
            for c in range(3):
                self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[9]').click()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).clear()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerFEDERAL.certiNumberFEDERAL)
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerFEDERAL.emitDateFEDERAL)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                sleep(t1)

                if self.onErrorDate(self.browser, XPATH_ERROR_EMIT, XPATH_CORRECTION):
                    continue

                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerFEDERAL.finalValidFEDERAL)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                sleep(t1)

                if not self.onErrorDate(self.browser, XPATH_ERROR_VALID, XPATH_CORRECTION):
                    break

            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)

        if 'municipal.pdf' in selectedFiles:
            pdfPathMunicipal = constructedFilePath('municipal.pdf')
            readerMUNICIPAL = ReaderPDF(pdfPathMunicipal)
            for c in range(3):
                self.browser.find_element(By.XPATH, XPATH_TIPO + '/option[2]').click()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).clear()
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_CERTI_BOX).send_keys(readerMUNICIPAL.certiNumberMUNICIPAL)
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).send_keys(readerMUNICIPAL.emitDateMUNICIPAL)
                self.browser.find_element(By.XPATH, XPATH_EMIT_BOX).click()
                sleep(t1)

                if self.onErrorDate(self.browser, XPATH_ERROR_EMIT, XPATH_CORRECTION):
                    continue
                    
                sleep(t1)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).clear()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).send_keys(readerMUNICIPAL.finalValidMUNICIPAL)
                self.browser.find_element(By.XPATH, XPATH_VALID_BOX).click()
                sleep(t1)

                if not self.onErrorDate(self.browser, XPATH_ERROR_VALID, XPATH_CORRECTION):
                    break

            self.browser.find_element(By.XPATH, XPATH_SAVE).click()
            sleep(t3)
            alert = self.browser.switch_to.alert
            alert.accept()
            sleep(t2)
            processedCount += 1
            if processedCount == numSelected:
                self.browser.find_element(By.XPATH, XPATH_INIT).click()
                sleep(t2)


    def quit_browser(self):
        if self.browser:
            self.browser.quit()

def getSitNumber():
    return input('Nº SIT: ')

# def dateConverter(data_str):
#     dia, mes_nome, ano = data_str.lower().split(' de ')
#     mes = MESES[mes_nome]
#     data = datetime(int(ano), mes, int(dia))
#     return data.strftime("%d/%m/%Y")