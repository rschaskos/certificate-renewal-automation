import re
import os
import io
import sys

from PyPDF2 import PdfReader
from src.patterns import CERTIFICATE_PATTERNS
from src.utils import constructedFilePath 

class ReaderPDF():
    def __init__(self, pathFile):
        self.pathFile = pathFile
        self.data = self._readerData()

        fileNameBase = os.path.basename(pathFile).split('.')[0].upper() 

        if fileNameBase not in CERTIFICATE_PATTERNS:
            self.certiNumber = None
            self.emitDate = None
            self.finalValid = None
            self.extractedData = {} 
            return 

        patternsForType = CERTIFICATE_PATTERNS[fileNameBase]

        # Extração dinâmica dos dados usando o método genérico
        self.certiNumber = self._extractDataFromPattern(patternsForType.get('certiNumber'))
        self.emitDate = self._extractDataFromPattern(patternsForType.get('emitDate'))
        self.finalValid = self._extractDataFromPattern(patternsForType.get('finalValid'))

        self.extractedData = {
            'certiNumber': self.certiNumber,
            'emitDate': self.emitDate,
            'finalValid': self.finalValid
        }
        
    def _readerData(self):
        data = ''
        oldStderr = sys.stderr
        sys.stderr = io.StringIO()

        try:
            with open(self.pathFile, 'rb') as file:
                reader = PdfReader(file)
                for row in reader.pages:
                    data += row.extract_text()
        except FileNotFoundError:
            print(f"Erro: Arquivo PDF não encontrado em {self.pathFile}")
        except Exception as e:
            print(f"Erro ao ler PDF {self.pathFile}: {e}")
        finally:
            sys.stderr = oldStderr
        return data

    # NOVO método genérico para extração de dados
    def _extractDataFromPattern(self, pattern):
        if not pattern: 
            return None
        pattern_match = re.search(pattern, self.data)
        if pattern_match:
            return pattern_match.group(1).strip() 
        return None

if __name__ == '__main__':
    
    fileFgts = constructedFilePath('fgts.pdf')
    readerFgts = ReaderPDF(fileFgts)
    if readerFgts.certiNumber: 
        print(f"FGTS - Número: {readerFgts.certiNumber}, Emissão: {readerFgts.emitDate}, Validade: {readerFgts.finalValid}")
    else:
        print(f"Não foi possível extrair dados do FGTS.pdf")

    fileTce = constructedFilePath('tce.pdf') 
    readerTce = ReaderPDF(fileTce)
    if readerTce.certiNumber:
        print(f"TCE - Número: {readerTce.certiNumber}, Emissão: {readerTce.emitDate}, Validade: {readerTce.finalValid}")
    else:
        print(f"Não foi possível extrair dados do TCE.pdf")

    fileEstadual = constructedFilePath('estadual.pdf') 
    readerEstadual = ReaderPDF(fileEstadual)
    if readerEstadual.certiNumber:
        print(f"ESTADUAL - Número: {readerEstadual.certiNumber}, Emissão: {readerEstadual.emitDate}, Validade: {readerEstadual.finalValid}")
    else:
        print(f"Não foi possível extrair dados do ESTADUAL.pdf")

    fileFederal = constructedFilePath('federal.pdf')
    readerFederal = ReaderPDF(fileFederal)
    if readerFederal.certiNumber:
        print(f'FEDERAL - Número: {readerFederal.certiNumber}, Emissãõ: {readerFederal.emitDate}, Validade: {readerFederal.finalValid}')
    else:
        print(f"Não foi possível extrair dados do FEDERAL.pdf")

    fileTrabalhista = constructedFilePath('federal.pdf')
    readerTrabalhista = ReaderPDF(fileTrabalhista)
    if readerTrabalhista.certiNumber:
        print(f'TRABALHISTA - Número: {readerTrabalhista.certiNumber}, Emissãõ: {readerTrabalhista.emitDate}, Validade: {readerTrabalhista.finalValid}')
    else:
        print(f"Não foi possível extrair dados do TRABALHISTA.pdf")

    fileMunicipal = constructedFilePath('Municipal.pdf')
    readerMunicipal = ReaderPDF(fileMunicipal)
    if readerMunicipal.certiNumber:
        print(f'MUNICIPAL - Número: {readerMunicipal.certiNumber}, Emissãõ: {readerMunicipal.emitDate}, Validade: {readerMunicipal.finalValid}')
    else:
        print(f"Não foi possível extrair dados do MUNICIPAL.pdf")

   