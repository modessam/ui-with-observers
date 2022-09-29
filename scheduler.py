import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QFileDialog, QComboBox,  QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QLineEdit
import openpyxl
import pandas as pd
from pycode import Monitor, Day, Task, process, read_input, arabic, \
    observer, khalafawy, road_el_farag, professor, Adoctor, doctor, manager, monitor0, monitors, days, \
    observser_data_lst

# 1
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("screen1.ui", self)

        self.inv = self.findChild(QPushButton, "inv")
        self.exam = self.findChild(QPushButton, "exam")

        self.inv.clicked.connect(self.invScreen)
        self.exam.clicked.connect(self.exScreen)

    def invScreen(self):
        widget.setCurrentWidget(invscreen1)

    def exScreen(self):
        widget.setCurrentWidget(exscreen1)

###############################################################################################################


class invScreen1(QWidget):
    def __init__(self):
        super(invScreen1, self).__init__()
        loadUi("screenInv1.ui", self)
        self.browse = self.findChild(QPushButton, "browse")
        self.generate = self.findChild(QPushButton, "generate")
        self.back = self.findChild(QPushButton, "back")
        self.label = self.findChild(QLabel, "lineEdit")

        self.browse.clicked.connect(self.browsefiles)
        self.generate.clicked.connect(self.generateTables)
        self.back.clicked.connect(self.goBack)

        self.txt = ""
        self.file_name = ""
    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls *xlsx )')
        self.lineEdit.setText(fname[0])
        self.txt = fname
        self.file_name = fname[0]

    def goBack(self):
        widget.setCurrentWidget(mainwindow)

    def generateTables(self):

        if (self.txt != ""):
            read_input(self.file_name)
            ok = process(monitors, days)
            cnt = 1
            if not ok:
                self.label_not_enough = self.findChild(QLabel,"label_not_enough")
                self.label_not_enough.setText("عدد المواظفين غير كافي")


            else:
                for mon in monitors:
                    mon.push_info(observser_data_lst, cnt)
                    #mon.print_info()
                    cnt = cnt + 1
                dataframeout = pd.DataFrame(observser_data_lst)
                dataframeout.to_excel("observer_output.xlsx")
                s2 = invScreen2()
                widget.addWidget(s2)
                widget.setCurrentWidget(s2)


# 3
class invScreen2(QWidget):
    def __init__(self):
        super(invScreen2, self).__init__()
        loadUi("screenInv2.ui", self)
        self.back = self.findChild(QPushButton, "back")
        self.back.clicked.connect(self.backfrominv_fun)

        self.browse = self.findChild(QPushButton, "browse")
        self.browse.clicked.connect(self.browsefiles)

        self.combox = self.findChild(QComboBox, "comboBox1")

        self.list = ["...اختار"]
        for mon in monitors:
            self.list.append(mon.user_name)

        self.combox.addItems(self.list)

        self.select = self.findChild(QPushButton, "select")
        self.select.clicked.connect(self.valueOfCombo)

        self.label_name = self.findChild(QLabel, "label_4")
        self.label_dep = self.findChild(QLabel, "label_6")

        self.table_widget = self.findChild(QTableWidget, "tableWidget")

        self.lineEdit = self.findChild(QLineEdit,"lineEdit")
        #self.search_value = self.lineEdit.text()
        self.searchButton = self.findChild(QPushButton,"searchButton")
        self.searchButton.clicked.connect(self.search_fun)

    def search_fun(self):

        if self.lineEdit.text() in self.list:

            self.index = self.list.index(self.lineEdit.text())-1
            self.load_data_search()

        else :
            self.lineEdit.setText("غير موجود")

        # clear combo
        self.combox.setCurrentIndex(0)


    def browsefiles(self):
        QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls *xlsx )')



    def valueOfCombo(self):
        # clear table rows
        for i in range(self.table_widget.rowCount()):
            self.table_widget.removeRow(self.table_widget.rowCount()-1)
        # clear labels
        self.label_name.setText("")
        self.label_dep.setText("")
        # clear search input
        self.lineEdit.setText("")
        # print(self.combox.currentIndex())
        if (self.combox.currentIndex()):

            self.load_data()   # add combobox value

    def load_data(self):
        mon = monitors[self.combox.currentIndex()-1]
        self.label_name.setText(mon.user_name)
        self.label_dep.setText(mon.title)
        for ts in mon.task:

            row = self.table_widget.rowCount()
            self.table_widget.setRowCount(row+1)

            self.table_widget.setItem(row,0,QTableWidgetItem(str(ts.day)))
            self.table_widget.setItem(row,1,QTableWidgetItem(str(ts.type)))
            self.table_widget.setItem(row,2,QTableWidgetItem(str(ts.building)))

    def load_data_search(self):
        # clear table rows
        for i in range(self.table_widget.rowCount()):
            self.table_widget.removeRow(self.table_widget.rowCount() - 1)
        # clear labels
        self.label_name.setText("")
        self.label_dep.setText("")
        mon = monitors[self.index]
        self.label_name.setText(mon.user_name)
        self.label_dep.setText(mon.title)
        for ts in mon.task:

            row = self.table_widget.rowCount()
            self.table_widget.setRowCount(row+1)

            self.table_widget.setItem(row,0,QTableWidgetItem(str(ts.day)))
            self.table_widget.setItem(row,1,QTableWidgetItem(str(ts.type)))
            self.table_widget.setItem(row,2,QTableWidgetItem(str(ts.building)))




    def backfrominv_fun(self):
        widget.setCurrentWidget(invscreen1)

###############################################################################################################
# 4
class exScreen1(QWidget):
    def __init__(self):
        super(exScreen1, self).__init__()
        loadUi("screenEx1.ui", self)
        self.browse = self.findChild(QPushButton, "browse")
        self.generate = self.findChild(QPushButton, "generate")
        self.back = self.findChild(QPushButton, "back")
        self.label = self.findChild(QLabel, "lineEdit")

        self.browse.clicked.connect(self.browsefiles)
        self.generate.clicked.connect(self.generateTables)
        self.back.clicked.connect(self.goBack)

        self.txt = ""

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls)')
        self.lineEdit.setText(fname[0])
        self.txt = fname

    def goBack(self):
        widget.setCurrentWidget(mainwindow)

    def generateTables(self):
        if (self.txt != ""):
            s1 = exScreen2()
            widget.addWidget(s1)
            widget.setCurrentWidget(s1)


# 5
class exScreen2(QWidget):

    def __init__(self):
        super(exScreen2, self).__init__()
        loadUi("screenEx2.ui", self)

        self.back = self.findChild(QPushButton, "back")
        self.back.clicked.connect(self.backfromex_fun)

        self.browse = self.findChild(QPushButton, "browse")
        self.browse.clicked.connect(self.browsefiles)
        #self.comboxlo = self.findChild(QComboBox, "comboBoxx1")
        #self.list1 = ["Rod Al-farag", "Khalfawy"]
        # self.comboxlo.addItems(self.list1)

        #self.comboxbu = self.findChild(QComboBox, "comboBoxx2")
        #self.list2 = ["Main builing", "Sub builing", ]
        # self.comboxbu.addItems(self.list2)

        self.comboxfl = self.findChild(QComboBox, "comboBoxx1_2")
        self.list3 = ["First floor", "Second floor", "third floor"]
        self.comboxfl.addItems(self.list3)

        # self.select1 = self.findChild(QPushButton, "select11")
        # self.select1.clicked.connect(self.valueOfCombo)

        # self.select2 = self.findChild(QPushButton, "select22")
        # self.select2.clicked.connect(self.valueOfCombo)

        # self.select3 = self.findChild(QPushButton, "select11_2")
        # self.select3.clicked.connect(self.valueOfCombo)

        self.table_widget = self.findChild(QTableWidget, "tableWidgetexam")

        self.label = self.findChild(QLabel, "label1")

    def browsefiles(self):
        QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv *xls)')

    def backfromex_fun(self):
        widget.setCurrentWidget(exscreen1)



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
exscreen1 = exScreen1()
invscreen1 = invScreen1()
widget.addWidget(mainwindow)
widget.addWidget(exscreen1)
widget.addWidget(invscreen1)
widget.setFixedWidth(780)
widget.setFixedHeight(690)
widget.show()
sys.exit(app.exec_())
