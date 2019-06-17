import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta


class SignUpWindow(QWidget):
    is_admin_signal = pyqtSignal()
    is_student_signal = pyqtSignal(str)
    is_signIn_signal = pyqtSignal()
    user_signup_signal = pyqtSignal(str)
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
        self.label_account = QLabel("账       号: ")
        self.label_account.setFont(labelFont)
        self.edit_account = QLineEdit()
        self.edit_account.setFont(lineEditFont)
        self.edit_account.setFixedHeight(28)
        self.edit_account.setFixedWidth(200)
        self.edit_account.setMaxLength(20)
        self.edit_account.setPlaceholderText('请输入账号')
        self.formlayout.addRow(self.label_account, self.edit_account)
        # 用户名以及输入框：
        self.label_userName = QLabel("用  户  名: ")
        self.label_userName.setFont(labelFont)
        self.edit_userName = QLineEdit()
        self.edit_userName.setFont(lineEditFont)
        self.edit_userName.setFixedHeight(28)
        self.edit_userName.setFixedWidth(200)
        self.edit_userName.setMaxLength(20)
        self.edit_userName.setPlaceholderText('请输入用户名')
        self.formlayout.addRow(self.label_userName, self.edit_userName)
        # 密码以及输入框
        self.label_passwd = QLabel("密       码: ")
        self.label_passwd.setFont(labelFont)
        self.edit_passwd = QLineEdit()
        self.edit_passwd.setFont(lineEditFont)
        self.edit_passwd.setFixedHeight(28)
        self.edit_passwd.setFixedWidth(200)
        self.edit_passwd.setMaxLength(16)
        self.edit_passwd.setEchoMode(QLineEdit.Password)
        self.edit_passwd.setPlaceholderText('请输入密码')
        self.formlayout.addRow(self.label_passwd, self.edit_passwd)
        # 确认密码以及输入框
        self.label_pass_again = QLabel("确认密码: ")
        self.label_pass_again.setFont(labelFont)
        self.edit_pass_again = QLineEdit()
        self.edit_pass_again.setFont(lineEditFont)
        self.edit_pass_again.setFixedHeight(28)
        self.edit_pass_again.setFixedWidth(200)
        self.edit_pass_again.setMaxLength(16)
        self.edit_pass_again.setEchoMode(QLineEdit.Password)
        self.edit_pass_again.setPlaceholderText('请输入用户名')
        self.formlayout.addRow(self.label_pass_again, self.edit_pass_again)
        # 登录button
        self.signIn = QPushButton('Login')
        self.signIn.setStyleSheet("QPushButton{background-color:rgb(95,158,160);border-radius:15px;}"
                                  "QPushButton:hover{background-color:rgb(100,184,255)}"
                                  "QPushButton:pressed{background-color:rgb(116,222,252)}")
        self.signIn.setFixedWidth(300)
        self.signIn.setFixedHeight(30)
        self.signIn.setFont(labelFont)

        self.signUp = QPushButton('SignUp')
        self.signUp.setStyleSheet("QPushButton{background-color:rgb(95,158,160);border-radius:15px;}"
                                  "QPushButton:hover{background-color:rgb(100,184,255)}"
                                  "QPushButton:pressed{background-color:rgb(116,222,252)}")
        self.signUp.setFixedWidth(300)
        self.signUp.setFixedHeight(30)
        self.signUp.setFont(labelFont)

        self.formlayout.addRow(self.signUp)
        self.formlayout.addRow(self.signIn)

        self.label = QLabel("欢迎加入图书大家庭哦")
        fontlabel = QFont("Microsoft YaHei")
        fontlabel.setPixelSize(30)

        self.label.setFont(fontlabel)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel{margin-top: 50px}")
        self.Hlayout1.addWidget(self.label)  # , Qt.AlignRight)

        self.widget1 = QWidget()
        self.widget1.setLayout(self.Hlayout1)

        self.widget2 = QWidget()
        self.widget2.setFixedWidth(330)
        self.widget2.setFixedHeight(250)
        self.widget2.setLayout(self.formlayout)
        self.Hlayout2.addWidget(self.widget2, Qt.AlignCenter)

        self.widget = QWidget()
        self.widget.setLayout(self.Hlayout2)

        self.Vlayout.addWidget(self.widget1)
        self.pic_label = QLabel()
        self.pic_label.setPixmap(QPixmap("./images/08.png").scaled(130, 113))
        self.pic_label.setAlignment(Qt.AlignCenter)
        self.Vlayout.addWidget(self.pic_label)

        self.Vlayout.addWidget(self.widget, Qt.AlignTop)
        self.Vlayout.addStretch(15)

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

        #reg_passwd = QRegExp("[a-zA-z0-9]+$")
        #pValidator.setRegExp(reg_passwd)
        self.edit_passwd.setValidator(pValidator)
        self.edit_userName.setValidator(pValidator)
        self.edit_pass_again.setValidator(pValidator)
        self.signIn.clicked.connect(self.checkIn)
        self.signUp.clicked.connect(self.doSignUp)
        #self.edit_account.returnPressed.connect(self.doSignUp)
        #self.edit_passwd.returnPressed.connect(self.doSignUp)
        #self.edit_userName.returnPressed.connect(self.doSignUp)
        #self.edit_pass_again.returnPressed.connect(self.doSignUp)

    def doSignUp(self):
        userId = self.edit_account.text()
        userName = self.edit_userName.text()
        password = self.edit_passwd.text()
        password_again = self.edit_pass_again.text()
        if userId == '' or password == '':
            print(QMessageBox.warning(self,"警告","账号和密码不能为空！",QMessageBox.Yes, QMessageBox.Yes))
            return
        if userName == '':
            print(QMessageBox.warning(self,"警告","请输入用户名！",QMessageBox.Yes, QMessageBox.Yes))
            return        
        if password_again == '':
            print(QMessageBox.warning(self,"警告","请确认您的密码！",QMessageBox.Yes, QMessageBox.Yes))
            return
        if password_again != password:
            print(QMessageBox.warning(self,"警告","两次输入的密码不一致！",QMessageBox.Yes, QMessageBox.Yes))
            return

        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM customer WHERE UserId='%s'" % (userId)
        query.exec_(sql)
        

        if (query.next()):
            print(QMessageBox.warning(self,"警告","该账号已存在, 请重新输入！",QMessageBox.Yes, QMessageBox.Yes))
            return
        db.commit()
        now = QDate.currentDate()
        sql = "INSERT INTO customer VALUES ('%s','%s','%s',0,0,'%s',0)" % (
                        userId, userName, password, now.toString(Qt.ISODate))
        db.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提醒", "恭喜,您已成功注册账号,欢迎加入我们!", QMessageBox.Yes, QMessageBox.Yes))
        self.user_signup_signal.emit(userId + '#' + '0')
        


    def checkIn(self):
        self.is_signIn_signal.emit()
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon("./images/icon.png"))
    mainMindow = SignUpWindow()
    mainMindow.show()
    sys.exit(app.exec_())
