import sys
from PySide6.QtWidgets import QApplication
from ui_splash import Splash
from ui_login import Login

app = QApplication(sys.argv)

login_window = None

splash = Splash()

def open_login():
    global login_window
    login_window = Login()
    login_window.show()
    splash.close()

splash.finished.connect(open_login)

splash.show()

sys.exit(app.exec())