'''
Aqui encontramos os patterns para buscar o RegEx dentro de cada pdf
'''

# FGTS

FGTS_PATTERN_CERTI = r'Certificação Número:\s(\d+)'
FGTS_PATTERN_EMIT = r'Informação obtida em\s(\d{2}/\d{2}/\d{4})'
FGTS_PATTERN_VALID = r'Validade:\d{2}/\d{2}/\d{4}\sa\s(\d{2}/\d{2}/\d{4})'

# ESTADUAL

ESTADUAL_PATTERN_CERTI = r'Nº\s*([^-]+\-\d+)'
ESTADUAL_PATTERN_EMIT = r'Emitido via Internet Pública \((\d{2}/\d{2}/\d{4})\s\d{2}:\d{2}:\d{2}\)'
ESTADUAL_PATTERN_VALID = r'Válida até\s(\d{2}/\d{2}/\d{4})'


# TCE

TCE_PATTERN_CERTI = r'Código de controle (\w+\.\w+\.\w+)(?=\s*Emitida)'
TCE_PATTERN_EMIT = r'Emitida em (\d{2}/\d{2}/\d{4})'
TCE_PATTERN_VALID = r'CERTIDÃO VÁLIDA ATÉ O DIA (\d{2}/\d{2}/\d{4})'


# TRABALHISTA

TRABALHISTA_PATTERN_CERTI = r'Certidão nº:\s*(\d+/\d{4})'
TRABALHISTA_PATTERN_EMIT = r'Expedição:\s*(\d{2}/\d{2}/\d{4})'
TRABALHISTA_PATTERN_VALID = r'Validade:\s*(\d{2}/\d{2}/\d{4})'


# FEDERAL

FEDERAL_PATTERN_CERTI = r'controle.*([0-9A-F]{4}\.[0-9A-F]{4}\.[0-9A-F]{4}\.[0-9A-F]{4})'
FEDERAL_PATTERN_EMIT = r'Emitida.*?dia\s+(\d{2}/\d{2}/\d{4})'
FEDERAL_PATTERN_VALID = r'até\s+(\d{2}/\d{2}/\d{4})'


# MUNICIPAL

MUNICIPAL_PATTERN_CERTI = r'Nº\s*(\d+/\d{4})'
MUNICIPAL_PATTERN_EMIT = r'Emitido por:.*(\d{2}/\d{2}/\d{4})'
MUNICIPAL_PATTERN_VALID = r'Validade até:\s*(\d{2}/\d{2}/\d{4})'