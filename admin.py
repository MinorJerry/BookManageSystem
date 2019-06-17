import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
import sip
from bookWidget import BookWidget
from bookInDialog import BookInDialog
from userManagement import UserManage
from bookOutDialog import BookOutDialog
class adminWidget(QWidget):
    is_exit_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Q版图书馆管理系统")
        self.resize(800,600)
        self.setFixedSize(self.width(), self.height())
        self.deleteBoookNo = ''
        self.userId = ''
        self.setUpUI()
    
    def setUpUI(self):
        font = QFont('Microsoft YaHei',16)
        self.global_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        #self.setLayout(self.global_layout)
        button_style = "QPushButton{background-color:rgb(100,184,255);border-radius:16px;}"+\
                       "QPushButton:hover{background-color:rgb(255,106,106)}" +\
                       "QPushButton:pressed{background-color:rgb(255,182,193)}"
        # 按键布局设计 左边一列
        self.userManageButton = QPushButton('用户管理')
        self.bookInButton = QPushButton('图书入库')
        self.bookOutButton = QPushButton('图书出库')
        self.bookInFromLocalButton = QPushButton('批量入库')
        self.exitButton = QPushButton('退出登录')
        

        self.userManageButton.setFixedSize(100,32)
        self.bookInButton.setFixedSize(100,32)
        self.bookOutButton.setFixedSize(100,32)
        self.bookInFromLocalButton.setFixedSize(100,32)
        self.exitButton.setFixedSize(100,32)

        self.userManageButton.setStyleSheet(button_style)
        self.bookInButton.setStyleSheet(button_style)
        self.bookOutButton.setStyleSheet(button_style)
        self.bookInFromLocalButton.setStyleSheet(button_style)
        self.exitButton.setStyleSheet(button_style)

        self.button_layout.addWidget(self.userManageButton)
        self.button_layout.addWidget(self.bookInButton)
        self.button_layout.addWidget(self.bookOutButton)
        self.button_layout.addWidget(self.bookInFromLocalButton)
        self.button_layout.addWidget(self.exitButton)

        # 总体布局 左边按钮 右边视图
        self.bookView = BookWidget()
        self.global_layout.addLayout(self.button_layout)
        self.global_layout.addWidget(self.bookView)

        # 按键与事件处理
        self.userManageButton.clicked.connect(self.userManage)
        self.bookInButton.clicked.connect(self.bookIn)
        self.bookOutButton.clicked.connect(self.bookOut)
        self.bookInFromLocalButton.clicked.connect(self.bookInFromLocal)
        self.exitButton.clicked.connect(self.exitLogin)
        self.bookView.tableView.clicked.connect(self.getDeleteBookInfo)
        #self.bookView.queryModel.itemClicked.connect(self.getDeleteBookInfo)
        
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

    def getDeleteBookInfo(self,item):
        row = self.bookView.tableView.currentIndex().row()
        self.bookView.tableView.verticalScrollBar().setSliderPosition(row)
        index = self.bookView.tableView.model().index(row,0)
        self.deleteBoookNo = self.bookView.tableView.model().data(index)
        #index = self.bookView.tableView.model().index(row,0)
        #print(self.bookView.tableView.model().data(index))

    def userManage(self):
        dialog = UserManage()
        dialog.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        dialog.show()
        dialog.exec_()
    
    def bookIn(self):
        dialog = BookInDialog()
        dialog.setUserId(self.userId)
        dialog.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        dialog.add_book_success_signal.connect(self.bookView.doSearch)
        dialog.show()
        dialog.exec_()

    def bookOut(self):
        if self.deleteBoookNo == '':
            print(QMessageBox.warning(self, "警告", "请选中要出库的书籍", QMessageBox.Yes, QMessageBox.Yes))
            return
        

        sql = "SELECT * FROM book WHERE BookNo='%s'" % self.deleteBoookNo
        
        self.db = QSqlDatabase.addDatabase("QMYSQL","bookOut")
        self.db.setDatabaseName('bookmanagement')
        self.db.setHostName('localhost')
        self.db.setUserName('root')
        self.db.setPassword('123456')
        self.db.open()
        query = QSqlQuery()
        query.exec_(sql)
        if query.next():
            dialog = BookOutDialog()
            dialog.setInfo(query.value(0),query.value(1),query.value(2),query.value(3),query.value(4),
                query.value(5))
            dialog.setUserId(self.userId)
            dialog.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            dialog.out_book_success_signal.connect(self.bookView.doSearch)
        self.db.commit()
        self.db.close()
        self.bookView.tableView.clearSelection()
        self.deleteBoookNo = ''
        #QSqlDatabase.removeDatabase('bookOut')
        dialog.show()
        dialog.exec_()
    
    def bookInFromLocal(self):
        fileName,fileType = QFileDialog.getOpenFileName(self,
                  "选取文件",
                  "./",
                  "Text Files (*.txt)")  #设置文件扩展名过滤,注意用双分号间隔
        f = open(fileName,"r")
        line  = f.readline()
        lineNo = 1
        self.db = QSqlDatabase.addDatabase("QMYSQL","bookFromLocal")
        self.db.setDatabaseName('bookmanagement')
        self.db.setHostName('localhost')
        self.db.setUserName('root')
        self.db.setPassword('123456')
        self.db.open()
        query = QSqlQuery()
        while line:
            #做sql的插入
            value = line.split()
            bookNo = value[0]
            bookName = value[1]
            publisher = value[2]
            year = value[3]
            author = value[4]
            edition = value[5]
            InNum = value[6]
            sql = "SELECT * FROM book WHERE BookNo = '%s'" % (bookNo)
            query.exec_(sql)
            success = 1
            if (query.next()):
                if query.value(1) != bookName:
                    print(QMessageBox.warning(self, "警告", "该编号已存在,但书名不对应！", QMessageBox.Yes, QMessageBox.Yes))
                    success = 0
                    break
                elif query.value(2) != publisher:
                    print(QMessageBox.warning(self, "警告", "该编号已存在,但出版社不对应！", QMessageBox.Yes, QMessageBox.Yes))
                    success = 0
                    break
                elif query.value(3) != int(year):
                    print(QMessageBox.warning(self, "警告", "该编号已存在,但出版日期不对应！", QMessageBox.Yes, QMessageBox.Yes))
                    success = 0
                    break
                elif query.value(4) != author:
                    print(QMessageBox.warning(self, "警告", "该编号已存在,但作者不对应！", QMessageBox.Yes, QMessageBox.Yes))
                    success = 0
                    break
                elif query.value(5) != edition:
                    print(QMessageBox.warning(self, "警告", "该编号已存在,但版本号不对应！", QMessageBox.Yes, QMessageBox.Yes))
                    success = 0
                    break
                

                sql = "UPDATE book SET TotalNum=TotalNum+%d,Num=Num+%d WHERE BookNo='%s'" % (
                    int(InNum), int(InNum), bookNo)
            else:
                sql = "INSERT INTO book VALUES ('%s','%s','%s',%d,'%s','%s',%d,%d)" % (
                    bookNo, bookName, publisher, int(year), author, edition, int(InNum), int(InNum))
            query.exec_(sql)
            self.db.commit()
            nowTime = QDate.currentDate().toString(Qt.ISODate)
            adminId = self.userId
            sql = "SELECT MAX(RecordId) FROM book_manage"
            query.exec_(sql)
            query.next()
            nowRecord = query.value(0)
            self.db.commit()
            sql = "INSERT INTO book_manage VALUES (%d,'%s','%s',1,%d,'%s')" % (nowRecord + 1, bookNo, adminId, int(InNum),nowTime)
            query.exec_(sql)
            self.db.commit()
            line = f.readline()
            lineNo += 1
        if success == 1:
            QMessageBox.information(self, "提示", "恭喜!添加书籍成功!", QMessageBox.Yes, QMessageBox.Yes)
        self.bookView.doSearch()
    def setUserId(self,userid):
        self.userId = userid
        db = QSqlDatabase.addDatabase("QMYSQL","setUserId")
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
    
    def exitLogin(self):
        if QMessageBox.information(self,"提示","你确定要退出登录吗？",
            QMessageBox.Yes | QMessageBox.No,QMessageBox.No) == QMessageBox.Yes:
            self.is_exit_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = adminWidget()
    mainMindow.show()
    sys.exit(app.exec_())