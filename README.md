<h1 align="center"> SCRIPT PARA AUTOMATIZAR TAREFAS REPETITIVAS EM UM SISTEMA WEB </h1>

## Descrição

Este script Python automatiza a inserção de dados de certificados (FGTS, Estadual, TCE, Trabalhista, Federal e Municipal) em um sistema web específico. Ele utiliza as bibliotecas PySide6 para a interface gráfica, Selenium para a automação web e PyPDF2 para extrair dados dos arquivos PDF.

## Pré-requisitos

Antes de começar, você precisa ter o Python 3.x instalado em sua máquina. Além disso, você precisará instalar as seguintes bibliotecas Python. Para instalá-las, abra o terminal e execute os comandos abaixo:

```
pip install PySide6
pip install selenium
pip install PyInstaller
pip install PyPDF2
pip install webdriver-manager # Para gerenciar automaticamente o driver do Chrome
```

## Explicação das bibliotecas adicionadas

PySide6: Necessária para criar a interface gráfica do aplicativo.
selenium: Utilizada para automatizar a interação com o navegador web.
PyInstaller: Usada para empacotar o script Python em um executável.
PyPDF2: Necessária para ler os dados dos arquivos PDF.
webdriver-manager: Facilita o gerenciamento do driver do Chrome, garantindo que a versão correta seja baixada automaticamente.

## Configuração

Arquivos PDF: Certifique-se de que os arquivos PDF (fgts.pdf, estadual.pdf, tce.pdf, trabalhista.pdf, federal.pdf, municipal.pdf) estejam localizados na mesma pasta que o script main.py ou o executável gerado.

## Como Executar

## Opção 1: Executar o script diretamente

Clone o repositório ou faça uma cópia do arquivo main.py em sua IDE favorita.

Certifique-se de que todas as bibliotecas listadas em "Pré-requisitos" estejam instaladas.

Execute o script. Na sua IDE, geralmente há um botão "Run" ou você pode usar o atalho de teclado apropriado.

Se preferir executar pelo terminal, navegue até o diretório onde o arquivo main.py está localizado.

Execute o script Python com o comando:
	
```
python main.py
```
	
## Opção 2: Executar o executável (após compilação com PyInstaller)

Se você tiver o PyInstaller instalado, pode compilar o script em um executável para facilitar a distribuição e execução.
Abra o terminal e navegue até o diretório do projeto.
Execute o seguinte comando para compilar o script (ajuste o caminho se necessário):
```
pyinstaller --clean --onedir --noconsole --icon=src/favicon.ico main.py --add-data "src:src"
```
Explicação das opções do PyInstaller:
--clean: Cria em executável limpo de caches
--onedir: Cria um arquivo executável com os diretórios separados.
--noconsole: Não exibe a janela do console.
--icon=src/favicon.ico: Define o ícone do executável.
--add-data "src:src": Inclui a pasta src e seu conteúdo no executável.

O executável será gerado na pasta dist.

Execute o arquivo .exe e mova os arquivos em .pdf para dentro da pasta "_internal"

## Funcionalidades

## Este código Python automatiza a inserção de dados de certificados em um sistema web, agilizando o processo e reduzindo o risco de erros manuais. As principais funcionalidades incluem

Interface Gráfica: Uma interface amigável construída com PySide6 permite ao usuário inserir as credenciais de login e selecionar os tipos de certificados a serem processados.
Login Automatizado: O script automatiza o processo de login no sistema web.
Navegação Automatizada: O script navega automaticamente até a página de inserção de dados dos certificados.
Extração de Dados dos PDFs: A biblioteca PyPDF2 é utilizada para extrair os dados relevantes (número do certificado, data de emissão, data de validade) dos arquivos PDF fornecidos.
Inserção Automática de Dados: O script insere automaticamente os dados extraídos dos PDFs nos campos apropriados do sistema web.
Suporte a Múltiplos Tipos de Certificados: O script suporta a inserção de dados para os seguintes tipos de certificados: FGTS, Estadual, TCE, Trabalhista, Federal e Municipal.
Gerenciamento de Drivers: O webdriver-manager gerencia a instalação e atualização do driver do Chrome.

## Observações

Certifique-se de que a estrutura dos arquivos PDF corresponde ao formato esperado pelo script.
O script foi desenvolvido para um sistema web específico. Adaptações podem ser necessárias para funcionar em outros sistemas.
A velocidade da automação pode ser ajustada nas variáveis t1, t2 e t3 no arquivo src/automaWeb.py (valores em segundos).

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões de melhorias, correções de bugs ou novas funcionalidades, sinta-se à vontade para abrir um pull request.  

## Trata-se de uma ferramenta para uso interno na organização, porém é possível usar com os conceitos empregados.
