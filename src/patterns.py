'''
Aqui encontramos os patterns para buscar o RegEx dentro de cada PDF
'''

CERTIFICATE_PATTERNS = {
    'FGTS': {
        'certiNumber': r'Certificação Número:\s(\d+)',
        'emitDate': r'Informação obtida em\s(\d{2}/\d{2}/\d{4})',
        'finalValid': r'Validade:\d{2}/\d{2}/\d{4}\sa\s(\d{2}/\d{2}/\d{4})'
    },
    'ESTADUAL': {
        'certiNumber': r'Nº\s*([^-]+\-\d+)',
        'emitDate': r'Emitido via Internet Pública \((\d{2}/\d{2}/\d{4})\s\d{2}:\d{2}:\d{2}\)',
        'finalValid': r'Válida até\s(\d{2}/\d{2}/\d{4})'
    },
    'TCE': {
        'certiNumber': r'Código de controle (\w+\.\w+\.\w+)(?=\s*Emitida)',
        'emitDate': r'Emitida em (\d{2}/\d{2}/\d{4})',
        'finalValid': r'\s*CER\s*TIDÃO\s*VÁLIDA\s*ATÉ\s*O\s*DIA\s*(\d{2}/\d{2}/\d{4})'
    },
    'TRABALHISTA': {
        'certiNumber': r'Certidão nº:\s*(\d+/\d{4})',
        'emitDate': r'Expedição:\s*(\d{2}/\d{2}/\d{4})',
        'finalValid': r'Validade:\s*(\d{2}/\d{2}/\d{4})'
    },
    'FEDERAL': {
        'certiNumber': r'controle.*([0-9A-F]{4}\.[0-9A-F]{4}\.[0-9A-F]{4}\.[0-9A-F]{4})',
        'emitDate': r'Emitida.*?dia\s+(\d{2}/\d{2}/\d{4})',
        'finalValid': r'até\s+(\d{2}/\d{2}/\d{4})'
    },
    'MUNICIPAL': {
        'certiNumber': r'Nº\s*(\d+/\d{4})',
        'emitDate': r'emitida em: (\d{2}/\d{2}/\d{4})',
        'finalValid': r'VALIDADE: (\d{2}/\d{2}/\d{4})'
    }
}

print(CERTIFICATE_PATTERNS['ESTADUAL'].get('certiNumber'))