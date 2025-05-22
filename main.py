import sys
import os

from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.mainWindow import MainWindow

current = Path(__file__).parent
os.chdir(current)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('src/favicon.ico'))
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
