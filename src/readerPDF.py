import re
import os
import io
import sys

from pathlib import Path
from PyPDF2 import PdfReader
from patterns import *
# from src.utils import constructedFilePath


current = Path(__file__).parent
parent = current.parent
os.chdir(parent)

class ReaderPDF():
    def __init__(self, pathFile):
        self.pathFile = pathFile
        self.data = self._readerData()
        self.certiNumberFGTS = self._extractCertiNumberFGTS()
        self.emitDateFGTS = self._extractEmitDateFGTS()
        self.finalValidFGTS = self._extractFinalValidFGTS()
        self.certiNumberESTADUAL = self._extractCertiNumberESTADUAL() 
        self.emitDateESTADUAL = self._extractEmitDateESTADUAL()
        self.finalValidESTADUAL = self._extractFinalValidESTADUAL()
        self.certiNumberTCE = self._extractCertiNumberTCE() 
        self.emitDateTCE = self._extractEmitDateTCE()
        self.finalValidTCE = self._extractFinalValidTCE()
        self.certiNumberTRABALHISTA = self._extractCertiNumberTRABALHISTA() 
        self.emitDateTRABALHISTA = self._extractEmitDateTRABALHISTA()
        self.finalValidTRABALHISTA = self._extractFinalValidTRABALHISTA()
        self.certiNumberFEDERAL = self._extractCertiNumberFEDERAL() 
        self.emitDateFEDERAL = self._extractEmitDateFEDERAL()
        self.finalValidFEDERAL = self._extractFinalValidFEDERAL()
        self.certiNumberMUNICIPAL = self._extractCertiNumberMUNICIPAL()
        self.emitDateMUNICIPAL = self._extractEmitNumberMUNICIPAL()
        self.finalValidMUNICIPAL = self._extractFinalNumberMUNICIPAL()
        
    def _readerData(self):
        data = ''
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()

        try:
            with open(self.pathFile, 'rb') as file:
                reader = PdfReader(file)
                for row in reader.pages:
                    data += row.extract_text()
        except FileNotFoundError:
            ...
            # print(f'Erro - arquivo não encontrado: {self.pathFile}')
            # print('Coloque os arquivos na mesma pasta do programa.')
        finally:
            sys.stderr = old_stderr
        return data
    

    # FGTS EXTRACTION
    def _extractCertiNumberFGTS(self):
        pattern_match = re.search(FGTS_PATTERN_CERTI, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractEmitDateFGTS(self):
        pattern_match = re.search(FGTS_PATTERN_EMIT, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
        
    def _extractFinalValidFGTS(self):
        pattern_match = re.search(FGTS_PATTERN_VALID, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    

    # ESTADUAL EXTRACTION   
    def _extractCertiNumberESTADUAL(self):
        pattern_match = re.search(ESTADUAL_PATTERN_CERTI, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractEmitDateESTADUAL(self):
        pattern_match = re.search(ESTADUAL_PATTERN_EMIT, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractFinalValidESTADUAL(self):
        pattern_match = re.search(ESTADUAL_PATTERN_VALID, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    
    # TCE EXTRACTION   
    def _extractCertiNumberTCE(self):
        pattern_match = re.search(TCE_PATTERN_CERTI, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractEmitDateTCE(self):
        pattern_match = re.search(TCE_PATTERN_EMIT, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractFinalValidTCE(self):
        pattern_match = re.search(TCE_PATTERN_VALID, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    

    # TRABALHISTA EXTRACTION   
    def _extractCertiNumberTRABALHISTA(self):
        pattern_match = re.search(TRABALHISTA_PATTERN_CERTI, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractEmitDateTRABALHISTA(self):
        pattern_match = re.search(TRABALHISTA_PATTERN_EMIT, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractFinalValidTRABALHISTA(self):
        pattern_match = re.search(TRABALHISTA_PATTERN_VALID, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None


    # FEDERAL EXTRACTION   
    def _extractCertiNumberFEDERAL(self):
        pattern_match = re.search(FEDERAL_PATTERN_CERTI, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractEmitDateFEDERAL(self):
        pattern_match = re.search(FEDERAL_PATTERN_EMIT, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractFinalValidFEDERAL(self):
        pattern_match = re.search(FEDERAL_PATTERN_VALID, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    

    # MUNICIPAL EXTRACTION   
    def _extractCertiNumberMUNICIPAL(self):
        pattern_match = re.search(MUNICIPAL_PATTERN_CERTI, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractEmitNumberMUNICIPAL(self):
        pattern_match = re.search(MUNICIPAL_PATTERN_EMIT, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _extractFinalNumberMUNICIPAL(self):
        pattern_match = re.search(MUNICIPAL_PATTERN_VALID, self.data)
        if pattern_match:
            return pattern_match.group(1)
        return None 
    

if __name__ == '__main__':    
    # file = constructedFilePath('municipal.pdf') 
    file = 'fgts.pdf'
    r1 = ReaderPDF(file)

    # print(r1.data)
    print(f'Número da Certidão: {r1.certiNumberFGTS}')
    print(f'Data de emissão: {r1.emitDateFGTS}')
    print(f'Validade Final: {r1.finalValidFGTS}')

