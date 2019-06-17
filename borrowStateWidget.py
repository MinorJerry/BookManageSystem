import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
import sip
from bookWidget import MySqlModel
class BorrowStateWidget(QWidget):
    is_return_signal = pyqtSignal()
    def __init__(self):
        super(BorrowStateWidget, self).__init__()
        self.resize(600, 500)
        self.setWindowTitle("Q版图书馆管理系统")  
        self.setFixedSize(self.width(), self.height())
        #self.queryModel = None
        #self.tableView = None
        self.userId = ''
        self.returnBookNo = ''
        self.rowCount = 0
        self.setUpUI()

    def setUpUI(self):
        self.global_layout = QVBoxLayout()
        font = QFont("Microsoft YaHei",20)
        self.borrowBookLabel = QLabel("未归还书籍:")
        self.borrowBookLabel.setFont(font)
        self.global_layout.addWidget(self.borrowBookLabel)
        db = QSqlDatabase.addDatabase("QMYSQL","bookStateWidget")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery()
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.rowCount)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['编号', '书名', '出版社', '作者', '版本', '借阅时间', '应还时间'])
        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 隐藏表头
        self.tableWidget.verticalHeader().hide()
        # 调整宽度
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.global_layout.addWidget(self.tableWidget)
        self.tableWidget.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        #sql = "SELECT * FROM book"
        
        # 归还按钮
        self.returnButton = QPushButton('归还书籍')
        self.returnButton.setFont(QFont('Microsoft YaHei',12))
        self.returnButton.setFixedHeight(32)
        self.returnButton.setFixedWidth(140)
        self.returnButton.setStyleSheet("QPushButton{background-color:rgb(100,184,255);border-radius:16px;}"
                                        "QPushButton:hover{background-color:rgb(255,106,106)}" 
                                        "QPushButton:pressed{background-color:rgb(255,182,193)}")
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.returnButton,Qt.AlignCenter)
        self.global_layout.addLayout(self.buttonLayout)
        # 推荐新的书籍
        self.recommentLabel = QLabel('好书快递:')
        self.recommentLabel.setFont(font)
        self.global_layout.addWidget(self.recommentLabel)

        self.newTableWidget = QTableWidget()
        self.newTableWidget.setRowCount(5)
        self.newTableWidget.setColumnCount(5)
        self.newTableWidget.setHorizontalHeaderLabels(['编号', '书名', '出版社', '作者', '版本'])
        # 不可编辑
        self.newTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.newTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.newTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 隐藏表头
        self.newTableWidget.verticalHeader().hide()
        # 调整宽度
        self.newTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.newTableWidget.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        sql = "SELECT BookNo,BookName,Publisher,Author,Edition FROM book WHERE num > 0 order by num limit 5"
        query.exec_(sql)
        nowLine = 0
        while query.next():
            for i in range(5):
                item = QTableWidgetItem(query.value(i))
                item.setTextAlignment(Qt.AlignCenter)
                self.newTableWidget.setItem(nowLine,i,item)
            nowLine += 1
        self.global_layout.addWidget(self.newTableWidget)

        self.setLayout(self.global_layout)
        self.returnButton.clicked.connect(self.returnBook)
        self.tableWidget.itemClicked.connect(self.getReturnBookInfo)

    def getReturnBookInfo(self):
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.verticalScrollBar().setSliderPosition(row)
        self.returnBookNo = self.tableWidget.item(row,0).text()
        
    def returnBook(self):
        if self.returnBookNo == '':
            QMessageBox.warning(self,"警告", "请选中一本要归还的书！", QMessageBox.Yes,QMessageBox.Yes)
            return
        db = QSqlDatabase.addDatabase("QMYSQL","returnBook")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery()
        sql = "SELECT BookName FROM book WHERE BookNo='%s'" % self.returnBookNo
        query.exec_(sql)
        query.next()
        returnBookName = query.value(0) 
        if QMessageBox.information(self,"提示", "您确定要归还\n%s吗？" % returnBookName, QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No) == QMessageBox.No:
            return
        # 更新book 表
        sql = "UPDATE book SET Num=Num+1 WHERE BookNo='%s'" % self.returnBookNo
        query.exec_(sql)
        db.commit()
        # 更新customer表
        sql = "UPDATE customer SET NumBorrowers=NumBorrowers-1 WHERE UserId='%s'" % self.userId
        query.exec_(sql)
        db.commit()
        # 更新borrow表
        sql = "DELETE FROM borrow WHERE BookNo='%s' AND UserId='%s'" % (self.returnBookNo,self.userId)
        self.tableWidget.clearSelection()
        self.returnBookNo = ''
        query.exec_(sql)
        db.commit()
        QMessageBox.information(self, "提示", "归还成功!", QMessageBox.Yes, QMessageBox.Yes)
        self.is_return_signal.emit()

    def getReturnDate(self,borrowDate):
        year, month, day = [int(i) for i in borrowDate.split('-')]
        if month <= 10:
            month += 2
            if day == 31 and (month == 4 or month == 6 or month == 9 or month == 11):
                day = 30
            return str(year) + '-' + "%02d"%month + '-' + "%02d"%day
        else : # month = 11 or 12
            year = year + 1
            month = (month + 2) % 13 + 1
            if month == 2 and day > 28:
                day = 28
            return str(year) + '-' + "%02d"%month + '-' + "%02d"%day

    def setUserId(self,userid):
        self.userId = userid
        db = QSqlDatabase.addDatabase("QMYSQL","borrowBookDisp")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery()
        sql = "SELECT b.BookNo,b.BookName,b.publisher,b.author,b.edition,bo.BorrowTime FROM book b,borrow bo WHERE b.BookNo = bo.BookNo AND bo.UserId = '%s'" % self.userId 
        query.exec_(sql)
        # 为表格添加数据
        while query.next():
            self.rowCount += 1
            self.tableWidget.setRowCount(self.rowCount)
            
            for i in range(7):
                if i == 6:
                    returnDate = self.getReturnDate(query.value(5))
                    item = QTableWidgetItem(returnDate)
                    nowDate = QDate.currentDate().toString(Qt.ISODate)
                    if nowDate > returnDate:
                        item.setForeground(QBrush(QColor(Qt.red)))
                else:
                    item = QTableWidgetItem(query.value(i))
                    item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(self.rowCount - 1,i,item)
                
        db.commit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BorrowStateWidget()
    mainMindow.show()
    sys.exit(app.exec_())