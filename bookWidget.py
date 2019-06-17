import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import qdarkstyle
import qtawesome as qta
import sip
class MySqlModel(QSqlQueryModel):
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return QSqlQueryModel.data(self,index,role)
        
class BookWidget(QWidget):
    def __init__(self):
        super(BookWidget, self).__init__()
        self.resize(600, 500)
        self.setWindowTitle("Q版图书馆管理系统")  
        self.setFixedSize(self.width(), self.height())
        self.queryModel = None
        self.tableView = None
        self.currentPage = 0
        self.totalPage = 0
        self.totalRecord = 0
        self.pageRecord = 10
        self.setUpUI()

    def setUpUI(self):
        self.global_layout = QVBoxLayout()
        self.Hlayout_search = QHBoxLayout()
        self.Hlayout_pageJump = QHBoxLayout()
        button_style = "QPushButton{background-color:rgb(100,184,255)}"+\
                       "QPushButton:hover{background-color:rgb(255,106,106)}" +\
                       "QPushButton:pressed{background-color:rgb(255,182,193)}"
        # 实现搜索功能 水平布局 最上面的一行
        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(32)
        self.searchEdit.setStyleSheet("QLineEdit { background-color: rgb(10,55,130); color: white; border: 1px solid rgb(50,65,75); }"
                                      "QLineEdit:hover{ border: 1px solid rgb(20,140,210); }")
        font = QFont("Microsoft YaHei")
        font.setPixelSize(12)
        self.searchEdit.setFont(font)

        self.searchButton = QPushButton("查询")
        self.searchButton.setFixedHeight(32)
        self.searchButton.setFont(font)
        self.searchButton.setIcon(QIcon(QPixmap("./images/search.png")))
        self.searchButton.setFixedWidth(70)
        self.searchButton.setStyleSheet("QPushButton{background-color:rgb(100,184,255);}"
                                        "QPushButton:hover{background-color:rgb(255,106,106)}" 
                                        "QPushButton:pressed{background-color:rgb(255,182,193)}")
        
        self.conditionComboBox = QComboBox()
        searchCondision = ['按书名查询', '按作者查询', '按出版社查询']
        self.conditionComboBox.setFixedHeight(32)
        self.conditionComboBox.setFont(font)
        self.conditionComboBox.addItems(searchCondision)
        
        f = open("QComboBox.txt","r")
        self.conditionComboBox.setStyleSheet(f.read())
        f.close()
        #self.conditionComboBox.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.Hlayout_search.addWidget(self.searchEdit)
        self.Hlayout_search.addWidget(self.searchButton)
        self.Hlayout_search.addWidget(self.conditionComboBox)

        # 实现页跳转功能 水平布局 最下面的一行
        font = QFont("Microsoft YaHei",10)
        self.jumpToLabel = QLabel("跳转到第")
        #self.jumpToLabel.setFixedWidth(100)
        self.jumpToLabel.setFont(font)
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(30)
        self.pageEdit.setFont(font)
        s = "/" + str(self.totalPage) + "页"
        self.pageLabel = QLabel(s)
        self.pageLabel.setFont(font)
        self.jumpToButton = QPushButton("跳转")
        self.jumpToButton.setFont(font)
        self.jumpToButton.setStyleSheet(button_style)
        self.prevButton = QPushButton("前一页")
        self.prevButton.setFixedWidth(60)
        self.prevButton.setFont(font)
        self.prevButton.setStyleSheet(button_style)
        self.backButton = QPushButton("后一页")
        self.backButton.setFixedWidth(60)
        self.backButton.setFont(font)
        self.backButton.setStyleSheet(button_style)

        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.jumpToLabel)
        Hlayout.addWidget(self.pageEdit)
        Hlayout.addWidget(self.pageLabel)
        Hlayout.addWidget(self.jumpToButton)
        Hlayout.addWidget(self.prevButton)
        Hlayout.addWidget(self.backButton)
        
        widget = QWidget()
        widget.setLayout(Hlayout)
        widget.setFixedWidth(350)
        self.Hlayout_pageJump.addWidget(widget)
        

        # tableView 把数据库搜索结果显示到中间界面
        # 书名，出版社，出版时间，作者，版本，图书总量，剩余可借
        db = QSqlDatabase.addDatabase("QMYSQL","bookWidget")
        db.setDatabaseName('bookmanagement')
        db.setHostName('localhost')
        db.setUserName('root')
        db.setPassword('123456')
        db.open()
        query = QSqlQuery()
        self.tableView = QTableView()
        #self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #自动调整
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers) #不可编辑
        self.tableView.verticalHeader().hide()
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
       
        self.tableView.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.queryModel = MySqlModel()#QSqlQueryModel() 
        
        self.tableView.setModel(self.queryModel)
        #self.tableView.setSortingEnabled(True)
        #self.tableView.sortByColumn(0,Qt.AscendingOrder)
        self.queryModel.setHeaderData(0, Qt.Horizontal, "编号")
        self.queryModel.setHeaderData(1, Qt.Horizontal, "书名")
        self.queryModel.setHeaderData(2, Qt.Horizontal, "出版社")
        self.queryModel.setHeaderData(3, Qt.Horizontal, "出版时间")
        self.queryModel.setHeaderData(4, Qt.Horizontal, "作者")
        self.queryModel.setHeaderData(5, Qt.Horizontal, "版本")
        self.queryModel.setHeaderData(6, Qt.Horizontal, "图书总量")
        self.queryModel.setHeaderData(7, Qt.Horizontal, "剩余可借")
        
        self.doSearch()
        self.global_layout.addLayout(self.Hlayout_search)
        self.global_layout.addWidget(self.tableView)
        self.global_layout.addLayout(self.Hlayout_pageJump)
        
        self.setLayout(self.global_layout)
        self.searchButton.clicked.connect(self.doSearch)
        self.prevButton.clicked.connect(self.prev)
        self.backButton.clicked.connect(self.back)
        self.jumpToButton.clicked.connect(self.jumpTo)
        self.searchEdit.returnPressed.connect(self.doSearch)

    def setButtonStatus(self):
        if(self.currentPage==self.totalPage):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(False)
        if(self.currentPage==1):
            self.backButton.setEnabled(True)
            self.prevButton.setEnabled(False)
        if(self.currentPage<self.totalPage and self.currentPage>1):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(True)

    def getTotalRecordCount(self):
        self.queryModel.setQuery("SELECT * FROM book")
        self.totalRecord = self.queryModel.rowCount()
        return

    def getPageCount(self):
        self.getTotalRecordCount()
        self.totalPage = (self.totalRecord // self.pageRecord) + 1
        return

    def recordQuery(self, index):
        sql = ""
        conditionChoice = self.conditionComboBox.currentText()
        if (conditionChoice == "按书名查询"):
            conditionChoice = 'BookName'
        elif (conditionChoice == "按作者查询"):
            conditionChoice = 'Author'
        elif (conditionChoice == '按出版社查询'):
            conditionChoice = 'Publisher'

        if (self.searchEdit.text() == ""):
            self.getPageCount()
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            conditionChoice = 'BookNo'
            sql = ("select * from book ORDER BY %s  limit %d,%d " % (conditionChoice,index, self.pageRecord))
            self.queryModel.setQuery(sql)
            self.setButtonStatus()
            return

        searchText = self.searchEdit.text()
        s = '%'
        #for i in range(0, len(temp)):
        #    s = s + temp[i] + "%"
        for t in searchText.split(' '):
            s = s + t + '%'

        sql = ("SELECT * FROM book WHERE %s LIKE '%s' ORDER BY %s " % (
            conditionChoice, s,conditionChoice))
        self.queryModel.setQuery(sql)
        self.totalRecord = self.queryModel.rowCount()
        # 当查询无记录时的操作
        if(self.totalRecord==0):
            print(QMessageBox.information(self,"提醒","很抱歉没有找到您想要的结果",QMessageBox.Yes,QMessageBox.Yes))
            
            self.getPageCount()
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            conditionChoice = 'BookNo'
            sql = ("select * from book ORDER BY %s  limit %d,%d " % (conditionChoice,index, self.pageRecord))
            self.queryModel.setQuery(sql)
            self.setButtonStatus()
            return

        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        label = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(label)
        sql = ("SELECT * FROM book WHERE %s LIKE '%s' ORDER BY %s LIMIT %d,%d " % (
            conditionChoice, s, conditionChoice,index, self.pageRecord))
        self.queryModel.setQuery(sql)
        self.setButtonStatus()
        return

    # 点击查询
    def doSearch(self):
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount()
        s = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(s)
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 向前翻页
    def prev(self):
        self.currentPage -= 1
        if (self.currentPage <= 1):
            self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 向后翻页
    def back(self):
        self.currentPage += 1
        if (self.currentPage >= int(self.totalPage)):
            self.currentPage = int(self.totalPage)
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 点击跳转
    def jumpTo(self):
        if (self.pageEdit.text().isdigit()):
            self.currentPage = int(self.pageEdit.text())
            if (self.currentPage > self.totalPage):
                self.currentPage = self.totalPage
            if (self.currentPage <= 1):
                self.currentPage = 1
        else:
            self.currentPage = 1
        index = (self.currentPage - 1) * self.pageRecord
        self.pageEdit.setText(str(self.currentPage))
        self.recordQuery(index)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BookWidget()
    mainMindow.show()
    sys.exit(app.exec_())

