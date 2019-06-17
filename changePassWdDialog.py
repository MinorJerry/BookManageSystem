import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
import sip

class ChangePassWdDialog(QDialog):
    def __init__(self, parent=None):
        super(ChangePassWdDialog, self).__init__(parent)
        self.resize(350,300)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('修改密码')
        self.userId = ''
        self.setUpUI()

    def setUpUI(self):
        self.global_layout = QFormLayout()
        self.setLayout(self.global_layout)
        self.global_layout.setVerticalSpacing(10)

        font = QFont('Microsoft YaHei',20)
        self.title = QLabel('密码修改：')
        self.title.setFont(font)
        # 表单左半边
        self.account_label = QLabel('账     号：')
        self.passWd_label = QLabel('旧 密 码：')
        self.newPassWd_label = QLabel('新 密 码：')
        self.confirmPW_label = QLabel('确认密码：')
        
        # 表单右半边
        self.account_edit = QLineEdit()
        self.passWd_edit = QLineEdit()
        self.newPassWd_edit = QLineEdit()
        self.confirmPW_edit = QLineEdit()
        self.account_edit.setEnabled(False)

        # 字体设置
        font = QFont('Microsoft YaHei',12)
        self.account_label.setFont(font)
        self.passWd_label.setFont(font)
        self.newPassWd_label.setFont(font)
        self.confirmPW_label.setFont(font)
        self.account_edit.setFont(font)
        self.passWd_edit.setFont(font)
        self.newPassWd_edit.setFont(font)
        self.confirmPW_edit.setFont(font)
        
        # 可输入字符设置
        pValidator = QRegExpValidator(self)
        reg_passwd = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg_passwd)
        self.passWd_edit.setValidator(pValidator)
        self.newPassWd_edit.setValidator(pValidator)
        self.confirmPW_edit.setValidator(pValidator)
        
        # 长度设置
        self.passWd_edit.setMaxLength(16)
        self.newPassWd_edit.setMaxLength(16)
        self.confirmPW_edit.setMaxLength(16)
        
        # 密码格式设置
        self.passWd_edit.setEchoMode(QLineEdit.Password)
        self.newPassWd_edit.setEchoMode(QLineEdit.Password)
        self.confirmPW_edit.setEchoMode(QLineEdit.Password)

        # 底部按钮
        self.changePWButton = QPushButton('修改密码')
        self.changePWButton.setFont(QFont('Microsoft YaHei',14))
        # 加到布局里面
        self.global_layout.addRow(self.title)
        self.global_layout.addRow(self.account_label,self.account_edit)
        self.global_layout.addRow(self.passWd_label,self.passWd_edit)
        self.global_layout.addRow(self.newPassWd_label,self.newPassWd_edit)
        self.global_layout.addRow(self.confirmPW_label,self.confirmPW_edit)
        self.global_layout.addRow(self.changePWButton)

        self.changePWButton.clicked.connect(self.doChangePW)
        self.account_edit.returnPressed.connect(self.doChangePW)
        self.passWd_edit.returnPressed.connect(self.doChangePW)
        self.newPassWd_edit.returnPressed.connect(self.doChangePW)
        self.confirmPW_edit.returnPressed.connect(self.doChangePW)

    def setUserId(self,userid):
        self.userId = userid
        self.account_edit.setText(self.userId)
    def doChangePW(self):
        userId = self.account_edit.text()
        oldPW = self.passWd_edit.text()
        newPW = self.newPassWd_edit.text()
        confirmPW = self.confirmPW_edit.text()

        if oldPW == '' or newPW == '' or confirmPW == '':
            QMessageBox.warning(self, "警告", "表单不能为空！", QMessageBox.Yes, QMessageBox.Yes)
            return

        db = QSqlDatabase.addDatabase("QMYSQL","changePSW")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery()

        sql = "SELECT Password FROM customer WHERE UserId = '%s'" % self.userId
        query.exec_(sql)
        query.next()
        if query.value(0) != oldPW:
            QMessageBox.warning(self, "警告", "您输入的密码错误！", QMessageBox.Yes, QMessageBox.Yes)
            return
        if newPW != confirmPW:
            QMessageBox.warning(self, "警告", "两次输入的密码不一致！", QMessageBox.Yes, QMessageBox.Yes)
            return
        
        if QMessageBox.information(self, "提示", "您确定要修改密码吗？", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.No:
            return
        db.commit()
        # 更新customer表:
        sql = "UPDATE customer SET Password = '%s' WHERE userId = '%s'" % (newPW,self.userId)
        query.exec_(sql)

        QMessageBox.information(self, "提示", "恭喜！密码修改成功！", QMessageBox.Yes, QMessageBox.Yes)
        db.commit()
        db.close()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = ChangePassWdDialog()
    mainMindow.show()
    sys.exit(app.exec_())