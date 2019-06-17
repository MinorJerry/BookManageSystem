import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
import sip

class BookOutDialog(QDialog):
    out_book_success_signal = pyqtSignal()
    def __init__(self, parent=None):
        super(BookOutDialog, self).__init__(parent)
        self.resize(420,350)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('图书出库')
        self.userId = ''
        self.setUpUI()

    def setUpUI(self):
        self.global_layout = QFormLayout()
        self.setLayout(self.global_layout)
        self.global_layout.setVerticalSpacing(10)
        
        self.titleLabel = QLabel("图书出库")
        # formlayout 表单的左半边：
        self.bookIdLabel = QLabel("编    号:")
        self.bookNameLabel = QLabel("书    名:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishYearLabel = QLabel("出版日期:")
        self.authorLabel = QLabel("作    者:")
        self.editionLabel = QLabel("版    本")
        self.outNumLabel = QLabel("出库数量:")

        # formlayout 表单的右半边：
        self.bookIdEdit = QLineEdit()
        self.bookNameEdit = QLineEdit()
        self.publisherEdit = QLineEdit()
        self.publishYearEdit = QLineEdit()
        #self.publishYearEdit = QDateTimeEdit()
        #self.publishYearEdit.setDisplayFormat('yyyy-mm-dd')
        self.authorEdit = QLineEdit()
        self.editionEdit = QLineEdit()
        self.outNumEdit = QLineEdit()
        self.outNumEdit.setValidator(QIntValidator())

        # 设置除了数量以外的都不可编辑
        self.bookIdEdit.setEnabled(False)
        self.bookNameEdit.setEnabled(False)
        self.publisherEdit.setEnabled(False)
        self.publishYearEdit.setEnabled(False)
        self.authorEdit.setEnabled(False)
        self.editionEdit.setEnabled(False)
        
        # 尾部出库按钮
        self.bookOutButton = QPushButton('出库')

        # 将以上控件加入表单布局
        self.global_layout.addRow(self.titleLabel)
        self.global_layout.addRow(self.bookIdLabel,self.bookIdEdit)
        self.global_layout.addRow(self.bookNameLabel,self.bookNameEdit)
        self.global_layout.addRow(self.publisherLabel,self.publisherEdit)
        self.global_layout.addRow(self.publishYearLabel,self.publishYearEdit)
        self.global_layout.addRow(self.authorLabel,self.authorEdit)
        self.global_layout.addRow(self.outNumLabel,self.outNumEdit)
        self.global_layout.addRow('',self.bookOutButton)

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
        self.outNumLabel.setFont(font_widget)

        self.bookNameEdit.setFont(font_widget)
        self.bookIdEdit.setFont(font_widget)
        self.authorEdit.setFont(font_widget)
        self.publisherEdit.setFont(font_widget)
        self.publishYearEdit.setFont(font_widget)
        self.outNumEdit.setFont(font_widget)
        self.editionEdit.setFont(font_widget)
        self.bookOutButton.setFont(font_widget)

        # 按钮设置
        self.bookOutButton.setFixedHeight(32)
        self.bookOutButton.setFixedWidth(140)
        self.bookOutButton.clicked.connect(self.doBookOut)

    def setInfo(self,bookNo,bookName,publisher,year,author,edition):
        self.bookIdEdit.setText(bookNo)
        self.bookNameEdit.setText(bookName)
        self.publisherEdit.setText(publisher)
        self.publishYearEdit.setText(str(year))
        self.authorEdit.setText(author)
        self.editionEdit.setText(edition)

    def doBookOut(self):
        bookNo = self.bookIdEdit.text()
        bookName = self.bookNameEdit.text()
        publisher = self.publisherEdit.text()
        year = self.publishYearEdit.text()
        author = self.authorEdit.text()
        edition = self.editionEdit.text()
        outNum = self.outNumEdit.text()
        if self.userId == '':
            QMessageBox.warning(self, "警告", "您没有权限！", QMessageBox.Yes, QMessageBox.Yes)
        if outNum == '':
            print(QMessageBox.warning(self, "警告", "请输入出库数量！", QMessageBox.Yes, QMessageBox.Yes))
            return 

        db = QSqlDatabase.addDatabase("QMYSQL","bookOutDialog")
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
            if int(outNum) > query.value(7):
                print(QMessageBox.warning(self, "警告", "出库数量不能大于剩余量！", QMessageBox.Yes, QMessageBox.Yes))
                return
        
            
        sql = "UPDATE book SET TotalNum=TotalNum-%d,Num=Num-%d WHERE BookNo='%s'" % (
            int(outNum), int(outNum), bookNo)
        
        query.exec_(sql)
        db.commit()
        # 如果该图书的总库存量为0，可以考虑从表中删除，也可以不用 让管理员直接去数据库处删除
        # 我们这里并不删除它 因为可能还有要还书的人
        # 插入book_manage表
        now = QDate.currentDate()
        # timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "SELECT MAX(RecordId) FROM book_manage"
        query.exec_(sql)
        query.next()
        nowRecord = query.value(0)
        db.commit()
        sql = "INSERT INTO book_manage VALUES (%d,'%s','%s',0,%d,'%s')" % (nowRecord + 1, bookNo, self.userId, int(outNum),now.toString(Qt.ISODate))
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提示", "恭喜!书籍出库成功!", QMessageBox.Yes, QMessageBox.Yes))
        self.out_book_success_signal.emit()
        self.close()
        self.bookIdEdit.clear()
        self.bookNameEdit.clear()
        self.publisherEdit.clear()
        self.publishYearEdit.clear()
        self.authorEdit.clear()
        self.editionEdit.clear()
        self.outNumEdit.clear()
        return
    
    def setUserId(self,userid):
        self.userId = userid
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BookOutDialog()
    mainMindow.show()
    sys.exit(app.exec_())

