import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
import sip

class BookInDialog(QDialog):
    add_book_success_signal = pyqtSignal()
    def __init__(self, parent=None):
        super(BookInDialog, self).__init__(parent)
        self.resize(350,350)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('图书入库')
        self.userId = ''
        self.setUpUI()

    def setUpUI(self):
        self.global_layout = QFormLayout()
        self.setLayout(self.global_layout)
        self.global_layout.setVerticalSpacing(10)
        
        self.titleLabel = QLabel("图书入库")
        # formlayout 表单的左半边：
        self.bookIdLabel = QLabel("编    号:")
        self.bookNameLabel = QLabel("书    名:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishYearLabel = QLabel("出版日期:")
        self.authorLabel = QLabel("作    者:")
        self.editionLabel = QLabel("版    本")
        self.addNumLabel = QLabel("入库数量:")

        # formlayout 表单的右半边：
        self.bookIdEdit = QLineEdit()
        self.bookNameEdit = QLineEdit()
        self.publisherEdit = QLineEdit()
        self.publishYearEdit = QLineEdit()
        #self.publishYearEdit = QDateTimeEdit()
        #self.publishYearEdit.setDisplayFormat('yyyy-mm-dd')
        self.authorEdit = QLineEdit()
        self.editionEdit = QLineEdit()
        self.addNumEdit = QLineEdit()
        self.addNumEdit.setValidator(QIntValidator())

        # 尾部入库按钮
        self.bookInButton = QPushButton('入库')

        # 将以上控件加入表单布局
        self.global_layout.addRow(self.titleLabel)
        self.global_layout.addRow(self.bookIdLabel,self.bookIdEdit)
        self.global_layout.addRow(self.bookNameLabel,self.bookNameEdit)
        self.global_layout.addRow(self.publisherLabel,self.publisherEdit)
        self.global_layout.addRow(self.publishYearLabel,self.publishYearEdit)
        self.global_layout.addRow(self.authorLabel,self.authorEdit)
        self.global_layout.addRow(self.editionLabel,self.editionEdit)
        self.global_layout.addRow(self.addNumLabel,self.addNumEdit)
        self.global_layout.addRow('',self.bookInButton)

        # 字体设置
        font_title = QFont('Microsoft YaHei',20)
        font_widget = QFont('Microsoft YaHei',12)
        self.setFont(font_widget)
        self.titleLabel.setFont(font_title)
        self.bookNameLabel.setFont(font_widget)
        self.bookIdLabel.setFont(font_widget)
        self.authorLabel.setFont(font_widget)
        self.publisherLabel.setFont(font_widget)
        self.publishYearLabel.setFont(font_widget)
        self.addNumLabel.setFont(font_widget)

        self.bookNameEdit.setFont(font_widget)
        self.bookIdEdit.setFont(font_widget)
        self.authorEdit.setFont(font_widget)
        self.publisherEdit.setFont(font_widget)
        self.publishYearEdit.setFont(font_widget)
        self.addNumEdit.setFont(font_widget)
        self.editionEdit.setFont(font_widget)
        self.bookInButton.setFont(font_widget)

        # 按钮设置
        self.bookInButton.setFixedHeight(32)
        self.bookInButton.setFixedWidth(140)
        self.bookInButton.clicked.connect(self.doBookIn)

    def doBookIn(self):
        bookNo = self.bookIdEdit.text()
        bookName = self.bookNameEdit.text()
        publisher = self.publisherEdit.text()
        year = self.publishYearEdit.text()
        author = self.authorEdit.text()
        edition = self.editionEdit.text()
        InNum = self.addNumEdit.text()
        if self.userId == '':
            QMessageBox.warning(self, "警告", "您没有权限！", QMessageBox.Yes, QMessageBox.Yes)
            return

        if bookName == '' or publisher == '' or year == '' or author == '' or edition == '' or InNum == '':
            print(QMessageBox.warning(self, "警告", "表单不能为空！", QMessageBox.Yes, QMessageBox.Yes))
            return 

        db = QSqlDatabase.addDatabase("QMYSQL","bookIn")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery()
        # 如果已存在，则update Book表的现存量，剩余可借量，不存在，则insert Book表，同时insert buyordrop表
        sql = "SELECT * FROM book WHERE bookNo = '%s'" % (bookNo)
        query.exec_(sql)
        if (query.next()):
            if query.value(1) != bookName:
                print(QMessageBox.warning(self, "警告", "该编号已存在,但书名不对应！", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif query.value(2) != publisher:
                print(QMessageBox.warning(self, "警告", "该编号已存在,但出版社不对应！", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif query.value(3) != int(year):
                print(QMessageBox.warning(self, "警告", "该编号已存在,但出版日期不对应！", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif query.value(4) != author:
                print(QMessageBox.warning(self, "警告", "该编号已存在,但作者不对应！", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif query.value(5) != edition:
                print(QMessageBox.warning(self, "警告", "该编号已存在,但版本号不对应！", QMessageBox.Yes, QMessageBox.Yes))
                return
            

            sql = "UPDATE book SET TotalNum=TotalNum+%d,Num=Num+%d WHERE BookNo='%s'" % (
                int(InNum), int(InNum), bookNo)
        else:
            sql = "INSERT INTO book VALUES ('%s','%s','%s',%d,'%s','%s',%d,%d)" % (
                bookNo, bookName, publisher, int(year), author, edition, int(InNum), int(InNum))
        query.exec_(sql)
        db.commit()
        # 插入book_manage表
        now = QDate.currentDate()
        # timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "SELECT MAX(RecordId) FROM book_manage"
        query.exec_(sql)
        query.next()
        nowRecord = query.value(0)
        db.commit()
        sql = "INSERT INTO book_manage VALUES (%d,'%s','%s',1,%d,'%s')" % (nowRecord + 1, bookNo, self.userId, int(InNum),now.toString(Qt.ISODate))
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提示", "恭喜!添加书籍成功!", QMessageBox.Yes, QMessageBox.Yes))
        self.add_book_success_signal.emit()
        self.close()
        self.bookIdEdit.clear()
        self.bookNameEdit.clear()
        self.publisherEdit.clear()
        self.publishYearEdit.clear()
        self.authorEdit.clear()
        self.editionEdit.clear()
        self.addNumEdit.clear()
        return

    def setUserId(self,userid):
        self.userId = userid
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BookInDialog()
    mainMindow.show()
    sys.exit(app.exec_())

