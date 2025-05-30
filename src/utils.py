import sys
import os

def getExecutableDir():
    """Retorna o diretório onde o executável principal ou o script está rodando."""
    if getattr(sys, 'frozen', False):
        # Executando como aplicativo empacotado (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # Executando como script Python
        # Retorna o diretório da pasta (raiz do projeto)
        # Assumindo que utils.py está em src/ e main.py está na raiz do projeto.
        return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def constructedFilePath(nameFile):
    """
    Construir o caminho para um arquivo, procurando primeiro no diretório do executável/script
    e, em seguida, no diretório de trabalho atual (útil para PyInstaller --onefile).
    """
    # 1. Tentar o diretório do executável/script (ou a raiz do projeto no modo script)
    exec_dir = getExecutableDir()
    path_in_exec_dir = os.path.join(exec_dir, nameFile)
    if os.path.exists(path_in_exec_dir):
        return path_in_exec_dir

    # 2. Tentar o diretório de trabalho atual (muitas vezes o diretório temporário do --onefile)
    current_working_dir = os.getcwd()
    path_in_cwd = os.path.join(current_working_dir, nameFile)
    if os.path.exists(path_in_cwd):
        return path_in_cwd

    # 3. Se não encontrado em nenhum dos locais esperados, retornar o caminho padrão no exec_dir.
    # Isso é útil para arquivos que serão CRIADOS (como config.ini ou key.key)
    # ou para casos onde o arquivo *deveria* estar no exec_dir mas não foi encontrado.
    return os.path.join(exec_dir, nameFile)