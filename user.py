import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
import sip
from bookWidget import BookWidget
from borrowStateWidget import BorrowStateWidget
from changePassWdDialog import ChangePassWdDialog
class userWidget(QWidget):
    is_exit_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Q版图书馆管理系统")
        self.resize(800,600)
        self.setFixedSize(self.width(), self.height())
        self.userId = ''
        self.borrowBoookNo = ''
        self.setUpUI()

    def setUpUI(self):
        font = QFont('Microsoft YaHei',16)
        self.global_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.setLayout(self.global_layout)
        button_style = "QPushButton{background-color:rgb(100,184,255);border-radius:16px;}"+\
                       "QPushButton:hover{background-color:rgb(255,106,106)}" +\
                       "QPushButton:pressed{background-color:rgb(255,182,193)}"
        # 按键布局设计 左边一列
        self.borrowButton = QPushButton('图书借阅')
        #self.returnButton = QPushButton('图书归还')
        self.stateButton = QPushButton('借阅状态')
        self.allBookButton = QPushButton('所有书籍')
        self.changePasswdButton = QPushButton('修改密码')
        self.exitButton = QPushButton('退出登录')

        
        self.borrowButton.setFixedSize(100,32)
        #self.returnButton.setFixedSize(100,40)
        self.stateButton.setFixedSize(100,32)
        self.allBookButton.setFixedSize(100,32)
        self.changePasswdButton.setFixedSize(100,32)
        self.exitButton.setFixedSize(100,32)
        self.borrowButton.setStyleSheet(button_style)
        self.stateButton.setStyleSheet(button_style)
        self.allBookButton.setStyleSheet(button_style)
        self.changePasswdButton.setStyleSheet(button_style)
        self.exitButton.setStyleSheet(button_style)

        self.button_layout.addWidget(self.borrowButton)
        #self.button_layout.addWidget(self.returnButton)
        self.button_layout.addWidget(self.stateButton)
        self.button_layout.addWidget(self.allBookButton)
        self.button_layout.addWidget(self.changePasswdButton)
        self.button_layout.addWidget(self.exitButton)

        # 总体布局 左边按钮 右边视图
        self.bookView = BookWidget()
        self.global_layout.addLayout(self.button_layout)
        self.global_layout.addWidget(self.bookView)

        # 按键与事件处理
        self.borrowButton.clicked.connect(self.borrowBook)
        #self.returnButton.clicked.connect(self.returnBook)
        self.stateButton.clicked.connect(self.bookState)
        self.allBookButton.clicked.connect(self.allBook)
        self.changePasswdButton.clicked.connect(self.changePassword)
        self.exitButton.clicked.connect(self.exitLogin)
        self.bookView.tableView.clicked.connect(self.getBorrowBookInfo)

        # 背景美化 我放在最后来写
        self.global_layout_background = QVBoxLayout()
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(
            QPixmap("./images/background.jpg").scaled(self.width(), self.height())))
        self.widget = QWidget()
        self.widget.setLayout(self.global_layout)
        self.widget.setPalette(window_pale)
        self.widget.setAutoFillBackground(True)
        self.global_layout_background.addWidget(self.widget)
        self.setLayout(self.global_layout_background)
        self.global_layout_background.setContentsMargins(0, 0, 0, 0)
    def setUserId(self,userId):
        self.userId = userId
        db = QSqlDatabase.addDatabase("QMYSQL","setUserIdUser")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery(db)
        sql = "SELECT UserName FROM customer WHERE UserId='%s'" % self.userId
        query.exec_(sql)
        query.next()
        self.loginInfo = QLabel('当前登录用户：\n%s' % query.value(0))
        db.commit()
        self.loginInfo.setFont(QFont('Microsoft YaHei',12))
        self.loginInfo.setStyleSheet("color: #FFFF00")
        self.loginInfo.setFixedSize(100,40)
        self.button_layout.addWidget(self.loginInfo)

    def getBorrowBookInfo(self,item):
        row = self.bookView.tableView.currentIndex().row()
        self.bookView.tableView.verticalScrollBar().setSliderPosition(row)
        index = self.bookView.tableView.model().index(row,0)
        self.borrowBoookNo = self.bookView.tableView.model().data(index)
    
    def getBorrowBookInfoFromRecomment(self):
        row = self.bookStateWidget.newTableWidget.currentIndex().row()
        self.bookStateWidget.newTableWidget.verticalScrollBar().setSliderPosition(row)
        self.borrowBoookNo = self.bookStateWidget.newTableWidget.item(row,0).text()


    def borrowBook(self):
        #dialog = BorrowBookDialog()
        if self.userId == '':
            return
        if self.borrowBoookNo == '':
            print(QMessageBox.warning(self, "警告", "请选中要借的书籍！", QMessageBox.Yes, QMessageBox.Yes))
            return
        sql = "SELECT * FROM book WHERE bookNo='%s'" % self.borrowBoookNo
        self.db = QSqlDatabase.addDatabase("QMYSQL","borrowBook")
        self.db.setDatabaseName('bookmanagement')
        self.db.setHostName('localhost')
        self.db.setUserName('root')
        self.db.setPassword('123456')
        self.db.open()
        query = QSqlQuery()
        query.exec_(sql)
        if query.next():
            if query.value(7) == 0:
                print(QMessageBox.warning(self, "警告", "该书籍已被借完,请耐心等待！", QMessageBox.Yes, QMessageBox.Yes))
                self.db.commit()
                self.db.close()
                return
            self.db.commit()
            # 查看borrow表中该用户是否借了该本书
            sql = "SELECT * FROM borrow WHERE BookNo = '%s' AND UserId = '%s'"%(self.borrowBoookNo,self.userId)
            query.exec_(sql)
            if query.next():
                print(QMessageBox.warning(self, "警告", "您已经借阅了该书籍！", QMessageBox.Yes, QMessageBox.Yes))
                self.db.commit()
                self.db.close()
                return
            self.db.commit()

            # 查看用户是否到达借书量的上限:
            sql = "SELECT count(*) FROM borrow WHERE userId = '%s'" % self.userId
            query.exec_(sql)
            query.next()
            if query.value(0) >= 5:
                print(QMessageBox.warning(self, "警告", "对不起,您的借书量达到上限（5本）！", QMessageBox.Yes, QMessageBox.Yes))
                self.db.commit()
                self.db.close()
                return
            self.db.commit()
            
            # 提示消息窗口
            sql = "SELECT BookName FROM book WHERE BookNo = '%s'" % self.borrowBoookNo
            query.exec_(sql)
            query.next()
            bookName = query.value(0)
            if QMessageBox.information(self, "提示", "您确定借阅\n%s吗？"%bookName, QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No) == QMessageBox.No:
                return 

            # 更新book表
            sql = "UPDATE book SET Num=Num-1 WHERE BookNo='%s'" % self.borrowBoookNo 
            query.exec_(sql)
            self.db.commit()

            # 更新customer表
            sql = "UPDATE customer SET TimesBorrows=TimesBorrows+1,Numborrowers=Numborrowers+1 WHERE UserId='%s'" % self.userId
            query.exec_(sql)
            self.db.commit()

            # 更新borrow表
            nowTime = QDate.currentDate().toString(Qt.ISODate)
            sql = "INSERT INTO borrow values('%s','%s','%s')" % (self.borrowBoookNo,self.userId,nowTime)
            query.exec_(sql)
            self.db.commit()
            print(QMessageBox.information(self, "提示", "恭喜,借阅成功！", QMessageBox.Yes, QMessageBox.Yes))
            try:
                self.bookView.doSearch()
                return
            except:
                pass
            
            self.bookState()
            return 

    def returnBook(self):
        pass

    def bookState(self):
        try:
            self.global_layout.removeWidget(self.bookView)
            sip.delete(self.bookView)
        except:
            pass
        try:
            self.global_layout.removeWidget(self.bookStateWidget)
            sip.delete(self.bookStateWidget)
        except:
            pass
        self.bookStateWidget = BorrowStateWidget()
        self.bookStateWidget.setUserId(self.userId)
        self.global_layout.addWidget(self.bookStateWidget)
        self.bookStateWidget.newTableWidget.itemClicked.connect(self.getBorrowBookInfoFromRecomment)
        self.bookStateWidget.is_return_signal.connect(self.bookState)

    def allBook(self):
        try:
            self.global_layout.removeWidget(self.bookStateWidget)
            sip.delete(self.bookStateWidget)
        except:
            pass
        try:
            self.global_layout.removeWidget(self.bookView)
            sip.delete(self.bookView)
        except:
            pass
        self.bookView = BookWidget()
        self.global_layout.addWidget(self.bookView)
        self.bookView.tableView.clicked.connect(self.getBorrowBookInfo)

    def changePassword(self):
        dialog = ChangePassWdDialog()
        dialog.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        dialog.setUserId(self.userId)
        dialog.show()
        dialog.exec_()

    def exitLogin(self):
        if QMessageBox.information(self,"提示","你确定要退出登录吗？",
            QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.Yes:
            self.is_exit_signal.emit()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = userWidget()
    mainMindow.show()
    sys.exit(app.exec_())


