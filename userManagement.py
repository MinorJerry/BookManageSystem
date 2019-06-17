import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time
import sip

class UserManage(QDialog):
    def __init__(self,parent=None):
        super(UserManage, self).__init__(parent)
        self.resize(380, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("用户管理")
        # 用户数
        self.userCount = 0
        self.deleteId = ""
        self.deleteName = ""
        self.setUpUI()

    def setUpUI(self):
        self.db = QSqlDatabase.addDatabase("QMYSQL","userManage")
        self.db.setDatabaseName('bookmanagement')
        self.db.setHostName('localhost')
        self.db.setUserName('root')
        self.db.setPassword('123456')
        self.db.open()
        self.query = QSqlQuery()
        self.getTotalInfo()
        self.setForm()

    def setForm(self):
        # 表格设置
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.userCount)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['账号', '用户名'])
        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.tableWidget)
        self.setRows()
        self.deleteUserButton = QPushButton("删 除 用 户")
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.deleteUserButton, Qt.AlignHCenter)
        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(48)
        font = QFont('Microsoft YaHei',15)
        self.deleteUserButton.setFixedHeight(36)
        self.deleteUserButton.setFixedWidth(180)
        self.deleteUserButton.setFont(font)
        self.layout.addWidget(self.widget, Qt.AlignCenter)
        # 设置信号
        self.deleteUserButton.clicked.connect(self.deleteUser)
        self.tableWidget.itemClicked.connect(self.getUserInfo)
        

    def getTotalInfo(self):
        sql = "SELECT COUNT(*) FROM customer WHERE IsAdmin=0"
        self.query.exec_(sql)
        self.userCount = 0
        if self.query.next():
            self.userCount = self.query.value(0)
        #while (self.query.next()):
        #    self.userCount += 1
        sql = "SELECT UserId,UserName FROM customer WHERE IsAdmin=0"
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.userCount):
            if (self.query.next()):
                UserIdItem = QTableWidgetItem(self.query.value(0))
                UserNameItem = QTableWidgetItem(self.query.value(1))
                UserIdItem.setFont(font)
                UserNameItem.setFont(font)
                UserIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                UserNameItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 0, UserIdItem)
                self.tableWidget.setItem(i, 1, UserNameItem)
        return

    def getUserInfo(self, item):
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.verticalScrollBar().setSliderPosition(row)
        self.getTotalInfo()
        """
        i = 0
        while (self.query.next() and i != row):
            i = i + 1
        """
        self.deleteId = self.tableWidget.item(row,0).text()
        self.deleteName = self.tableWidget.item(row,1).text()

    def deleteUser(self):
        if (self.deleteId == "" and self.deleteName == ""):
            print(QMessageBox.warning(self, "警告", "请选中要删除的用户", QMessageBox.Yes, QMessageBox.Yes))
            return
        """
        elif (self.deleteId == self.oldDeleteId and self.deleteName == self.oldDeleteName):
            print(QMessageBox.warning(self, "警告", "请选中要删除的用户", QMessageBox.Yes, QMessageBox.Yes))
            return
        """
        
        if (QMessageBox.information(self, "提醒", "删除用户:%s,%s\n用户一经删除将无法恢复，是否继续?" % (self.deleteId, self.deleteName),
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No) == QMessageBox.No):
            return
        # 从User表删除用户
        """
        sql = "DELETE FROM Customer WHERE UserId='%s'" % (self.deleteId)
        self.query.exec_(sql)
        self.db.commit()
        """
        # 归还所有书籍 这里需要修改 不是归还书籍 如果有借书的就不能删除该用户
        sql = "SELECT * FROM borrower  WHERE UserId='%s'" % self.deleteId
        self.query.exec_(sql)
        if self.query.next():
            print(QMessageBox.warning(self, "警告", "该用户有书籍未归还，无法删除！", QMessageBox.Yes, QMessageBox.Yes))
            return 
        # 如果没有在借的书籍 可以删除该用户
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "DELETE FROM customer WHERE UserId='%s'" % (self.deleteId)
        self.query.exec_(sql)
        self.db.commit()
        """
        updateBook=QSqlQuery()
        while (self.query.next()):
            bookNo=self.query.value(1)
            sql="UPDATE book SET Num=Num+1 WHERE BookNo='%s'"% bookNo
            updateBook.exec_(sql)
            self.db.commit()
        """
        """
        sql="UPDATE User_Book SET ReturnTime='%s',BorrowState=0 WHERE UserId='%s' AND BorrowState=1"%(timenow,self.deleteId)
        self.query.exec_(sql)
        self.db.commit()
        """
        self.tableWidget.clearSelection()
        self.deleteId = ''
        print(QMessageBox.information(self,"提醒","删除用户成功!",QMessageBox.Yes,QMessageBox.Yes))
        self.updateUI()
        return

    def updateUI(self):
        self.getTotalInfo()
        self.layout.removeWidget(self.widget)
        self.layout.removeWidget(self.tableWidget)
        sip.delete(self.widget)
        sip.delete(self.tableWidget)
        self.setForm()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = UserManage()
    mainMindow.show()
    sys.exit(app.exec_())