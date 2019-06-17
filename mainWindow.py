import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
from SignIn import SignInWindow
from SignUp import SignUpWindow
from admin import adminWidget
from user import userWidget
import sip
import traceback
class MainWindow(QMainWindow):
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)

        self.widget = SignInWindow()
        self.resize(800,600)
        self.setWindowTitle("Q版图书馆管理系统")
        self.setCentralWidget(self.widget)
        self.widget.is_signup_signal.connect(self.signUp)
        self.widget.is_user_signal.connect(self.userWindow)
        self.widget.is_admin_signal.connect(self.userWindow)

    def signUp(self):
        sip.delete(self.widget)
        self.widget = SignUpWindow()
        self.setCentralWidget(self.widget)
        self.widget.is_signIn_signal.connect(self.signIn)
        self.widget.user_signup_signal.connect(self.userWindow)
    
    def signIn(self):
        sip.delete(self.widget)
        self.widget = SignInWindow()
        self.setCentralWidget(self.widget)
        self.widget.is_signup_signal.connect(self.signUp)
        self.widget.is_user_signal.connect(self.userWindow)
        self.widget.is_admin_signal.connect(self.userWindow)

    def userWindow(self,userInfo):
        
        info = userInfo.split('#')
        userId = info[0]
        isAdmin = int(info[1])
        sip.delete(self.widget)
        if isAdmin:
            self.widget = adminWidget()
            
            self.setCentralWidget(self.widget)
            self.widget.setUserId(userId)
            self.widget.is_exit_signal.connect(self.signIn)
        else:
            self.widget = userWidget()
            self.setCentralWidget(self.widget)
            self.widget.setUserId(userId)
            self.widget.is_exit_signal.connect(self.signIn)
        
        

if __name__ == "__main__":
    app = 0
    app = QApplication(sys.argv)
    
    app.setWindowIcon(QIcon("./images/icon.png"))
    mainMindow = MainWindow()
    mainMindow.show()
    sys.exit(app.exec_())
