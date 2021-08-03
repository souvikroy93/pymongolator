import src.main
from src.main import WelcomeWindow
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WelcomeWindow()
    win.show()
    sys.exit(app.exec_())
