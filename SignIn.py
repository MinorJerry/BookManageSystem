import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
import sip

class SignInWindow(QWidget):
    is_admin_signal = pyqtSignal(str)
    is_user_signal = pyqtSignal(str)
    is_signup_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Q版图书馆管理系统")
        self.setFixedSize(self.width(), self.height())
        self.setUpUI()

    def setUpUI(self):
        self.Vlayout = QVBoxLayout()
        self.Vlayout1 = QVBoxLayout()
        self.Vlayout2 = QVBoxLayout(self)
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.formlayout = QFormLayout()
        self.formlayout.setVerticalSpacing(18)

        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(
            QPixmap("./images/background.jpg").scaled(self.width(), self.height())))
        

        labelFont = QFont("Microsoft YaHei")
        labelFont.setPixelSize(20)

        lineEditFont = QFont("Microsoft YaHei")
        lineEditFont.setPixelSize(16)

        passwordFont = QFont("Microsoft YaHei")
        passwordFont.setPixelSize(12)
        # 账号以及输入框：
        self.label_account = QLabel("账号: ")
        self.label_account.setFont(labelFont)
        self.edit_account = QLineEdit()
        self.edit_account.setFont(lineEditFont)
        self.edit_account.setFixedHeight(28)
        self.edit_account.setFixedWidth(200)
        self.edit_account.setMaxLength(20)
        self.edit_account.setPlaceholderText('请输入账号')
        self.formlayout.addRow(self.label_account, self.edit_account)
        # 密码以及输入框
        self.label_passwd = QLabel("密码: ")
        self.label_passwd.setFont(labelFont)
        self.edit_passwd = QLineEdit()
        self.edit_passwd.setFont(lineEditFont)
        self.edit_passwd.setFixedHeight(28)
        self.edit_passwd.setFixedWidth(200)
        self.edit_passwd.setMaxLength(16)
        self.edit_passwd.setEchoMode(QLineEdit.Password)
        self.edit_passwd.setPlaceholderText('请输入密码')
        self.formlayout.addRow(self.label_passwd, self.edit_passwd)

        # 登录button
        self.signIn = QPushButton('Login')
        self.signIn.setStyleSheet("QPushButton{background-color:rgb(95,158,160);border-radius:15px;}"
                                  "QPushButton:hover{background-color:rgb(100,184,255)}"
                                  "QPushButton:pressed{background-color:rgb(116,222,252)}")
        self.signIn.setFixedWidth(260)
        self.signIn.setFixedHeight(30)
        self.signIn.setFont(labelFont)

        self.signUp = QPushButton('SignUp')
        self.signUp.setStyleSheet("QPushButton{background-color:rgb(95,158,160);border-radius:15px;}"
                                  "QPushButton:hover{background-color:rgb(100,184,255)}"
                                  "QPushButton:pressed{background-color:rgb(116,222,252)}")
        self.signUp.setFixedWidth(260)
        self.signUp.setFixedHeight(30)
        self.signUp.setFont(labelFont)


        self.formlayout.addRow(self.signIn)
        self.formlayout.addRow(self.signUp)

        self.label = QLabel("欢迎使用图书管理系统")
        fontlabel = QFont("Microsoft YaHei")
        fontlabel.setPixelSize(30)

        self.label.setFont(fontlabel)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel{margin-top: 100px}")
        self.Hlayout1.addWidget(self.label)  # , Qt.AlignRight)

        self.widget1 = QWidget()
        self.widget1.setLayout(self.Hlayout1)

        self.widget2 = QWidget()
        self.widget2.setFixedWidth(300)
        self.widget2.setFixedHeight(150)
        self.widget2.setLayout(self.formlayout)
        self.Hlayout2.addWidget(self.widget2, Qt.AlignCenter)

        self.widget = QWidget()
        self.widget.setLayout(self.Hlayout2)

        self.Vlayout.addWidget(self.widget1)
        self.pic_label = QLabel()
        self.pic_label.setPixmap(QPixmap("./images/08.png").scaled(130, 113))
        self.pic_label.move(100,100)
        self.pic_label.setAlignment(Qt.AlignCenter)
        self.Vlayout.addWidget(self.pic_label)

        self.Vlayout.addWidget(self.widget, Qt.AlignTop)
        self.Vlayout.addStretch(23)

        self.widget3 = QWidget()
        self.widget3.setLayout(self.Vlayout)
        self.widget3.setPalette(window_pale)
        self.widget3.setAutoFillBackground(True)

        self.Vlayout2.addWidget(self.widget3)
        self.Vlayout2.setContentsMargins(0, 0, 0, 0)

        # 布局完成,对输入的账号密码进行校验
        reg_account = QRegExp("[a-zA-z0-9]+$")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg_account)
        self.edit_account.setValidator(pValidator)

        reg_passwd = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg_passwd)
        self.edit_passwd.setValidator(pValidator)
        self.signIn.clicked.connect(self.checkIn)
        self.signUp.clicked.connect(self.go2signup)
        #self.edit_passwd.returnPressed.connect(self.checkIn)
        #self.edit_account.returnPressed.connect(self.checkIn)

    def go2signup(self):
        self.is_signup_signal.emit()
        return
        
    def checkIn(self):
        UserId = self.edit_account.text()
        password = self.edit_passwd.text()
        if (UserId == "" or password == ""):
            print(QMessageBox.warning(self, "警告", "学号和密码不可为空!", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 打开数据库连接
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM customer WHERE UserId='%s'" % (UserId)
        query.exec_(sql)
        db.commit()
        
        
        if (not query.next()):
            print(QMessageBox.information(self, "提示", "该账号不存在!", QMessageBox.Yes, QMessageBox.Yes))
        else:
            if (UserId == query.value(0) and password == query.value(2)):
                # 如果是管理员
                if (query.value(6) == True):
                    self.is_admin_signal.emit(UserId + '#' + '1')
                    
                else:
                    self.is_user_signal.emit(UserId + '#' + '0')
                    
            else:
                print(QMessageBox.information(self, "提示", "密码错误!", QMessageBox.Yes, QMessageBox.Yes))
        
        return

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/icon.png"))
    mainMindow = SignInWindow()
    mainMindow.show()
    sys.exit(app.exec_())
