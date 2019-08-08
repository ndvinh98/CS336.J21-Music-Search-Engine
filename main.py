# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Desktop\NguyenDinhVinh-16521582\NguyenDinhVinh-16521582\UI\design_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import glob
from collections import Counter
from collections import defaultdict
import math
import sys
import json
import time
import webbrowser
from underthesea import word_tokenize
from textprocessing import caculate_tf, caculate_idf, caculate_query_weight, textprocessing, queryprocessing, normalize_query, caculate_score


#region Load Data 

query=""
check=0 #nếu check=1 thì search by lyric, check=2 search by name
lyric_show="" 
title_show=""
link_show=""

#load json datasets
with open('./data/original_datasets.json') as obj:
  original_datasets=json.load(obj)
with open('./data/original_names.json') as obj:
  original_names=json.load(obj)

#load danh sách iverted index của lời bài hát
with open('./data/Inverted_Index_Lyrics.json') as obj:
  #load file json sẽ tự động chuyển key của dict từ kiểu int sang string nên phải dùng object_hook để dữ nguyên kiểu dữ liệu
  #https://stackoverflow.com/questions/45068797/how-to-convert-string-int-json-into-real-int-with-json-loads
   inv_index=json.load(obj,object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})

#load danh sách inverted index của tên bài hát
with open('./data/Inverted_Index_Names.json') as obj:
   inv_index_names=json.load(obj,object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})


#load danh sách lengths của lời bài hát tương ứng với docID
with open('./data/Lengths_Lyrics.json') as obj:
  Lengths_Lyrics=json.load(obj,object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})

#load danh sách lengths của tên bài hát tương ứng với docID
with open('./data/Lengths_Names.json') as obj:
  Lengths_Names=json.load(obj,object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})


#endregion

class Ui_result_window(object):
    '''Cửa sổ display kết quả của truy vấn nhập vào'''
    def open_url(self,qmodelindex):
          '''Mở link bài hát tương ứng với Item  trong listwidget khi click'''
          global lyric_show
          global title_show
          global link_show
          item = self.listWidget.currentItem()
          title_show=item.text()
          

          
          if item.text() in original_datasets.keys():
            data=original_datasets[item.text()]['data']
            for url, lyrics in data.items():
                link_show=url
                lyric_show=lyrics      

            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_show_lyric()
            self.ui.setupUi(self.window)
            self.window.show()   

    def setupUi(self, result_window):
        '''xây dựng giao diện'''
        result_window.setObjectName("result_window")
        result_window.resize(1008, 652)
        self.centralwidget = QtWidgets.QWidget(result_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 501, 81))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 130, 200, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(340, 130, 250, 21))
        self.label_3.setObjectName("label_3")
        font_label = QtGui.QFont()
        font_label.setPointSize(10)
        self.label_3.setFont(font_label)
        self.label_2.setFont(font_label)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 170, 951, 451))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.listWidget.setFont(font)
        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.listWidget.setMovement(QtWidgets.QListView.Static)
        self.listWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setModelColumn(0)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setBatchSize(100)
        self.listWidget.setSpacing(14)
        self.listWidget.setWordWrap(False)
        self.listWidget.setSelectionRectVisible(False)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        result_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(result_window)
        self.statusbar.setObjectName("statusbar")
        result_window.setStatusBar(self.statusbar)

        self.retranslateUi(result_window)
        QtCore.QMetaObject.connectSlotsByName(result_window)

        pixmap = QPixmap('./UI/logo2.png')
        self.label.setPixmap(pixmap)
        self.label.setAlignment(QtCore.Qt.AlignLeft)

    def retranslateUi(self, result_window):
        '''Tính toán kết quả và in ra window'''
        _translate = QtCore.QCoreApplication.translate
        start_time = time.time()

        #xử lý chuỗi người dùng nhập vào
        global query
        query = queryprocessing(inv_index,word_tokenize(query, format='text'))#ViTokenizer.tokenize(query))

        #tính trọng số của query
        if(check==1): #search by lyric
          list_query=caculate_query_weight(query,inv_index,len(original_datasets))
          #Chuẩn hoá query
          list_query=normalize_query(list_query)
          #tính score và sắp xếp kq
          scores=caculate_score(list_query,inv_index,len(original_datasets),Lengths_Lyrics)
          count_result=0
          for index, score in scores:
              if score == 0:
                  break
              count_result+=1
        if(check==2): #search by name
          list_query=caculate_query_weight(query,inv_index_names,len(original_datasets))
          #Chuẩn hoá query
          list_query=normalize_query(list_query)
          #tính score và sắp xếp kq
          scores=caculate_score(list_query,inv_index_names,len(original_datasets),Lengths_Names)
          count_result=0
          for index, score in scores:
              if score == 0:
                  break
              count_result+=1

        result_window.setWindowTitle(_translate("result_window", "result"))
        self.label_2.setText(_translate("result_window", "Kết quả tìm thấy: "+str(count_result)))
        self.label_3.setText(_translate("result_window", "Thời gian tìm kiếm: "+str(time.time() - start_time)+" seconds"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

      
        #in kết quả ra màn hình
        i=0
        for index, score in scores[:20]:
            if score == 0:
                break
            item = self.listWidget.item(i)
            i+=1
            item.setText(_translate("result_window",original_names[index]))

        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.listWidget.clicked.connect(self.open_url)


class Ui_show_lyric(object):
    '''Cửa sổ display lyrics khi ta nhấn vào tên bài hát'''
    def setupUi(self, show_lyric):
        show_lyric.setObjectName("show_lyric")
        show_lyric.resize(983, 879)
        self.centralwidget = QtWidgets.QWidget(show_lyric)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(11, -1, -1, -1)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 938, 1541))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tittle = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Bree Serif")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tittle.setFont(font)
        self.tittle.setAlignment(QtCore.Qt.AlignCenter)
        self.tittle.setObjectName("tittle")
        self.gridLayout_2.addWidget(self.tittle, 0, 0, 1, 1)
        self.lyrics = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setItalic(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.lyrics.setFont(font)
        self.lyrics.setObjectName("lyrics")
        self.gridLayout_2.addWidget(self.lyrics, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        show_lyric.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(show_lyric)
        self.statusbar.setObjectName("statusbar")
        show_lyric.setStatusBar(self.statusbar)

        self.retranslateUi(show_lyric)
        QtCore.QMetaObject.connectSlotsByName(show_lyric)

        self.pushButton.clicked.connect(self.openurl)

    def openurl(self):
      webbrowser.open(link_show)

    def retranslateUi(self, show_lyric):
        _translate = QtCore.QCoreApplication.translate
        show_lyric.setWindowTitle(_translate("show_lyric", "show lyric"))
        self.tittle.setText(_translate("show_lyric", title_show))
        self.lyrics.setText(_translate("show_lyric", lyric_show))
        self.pushButton.setText(_translate("show_lyric", "CLICK ĐỂ NGHE NHẠC ONLINE"))


class Ui_Form(object):
    '''Main windows'''
    def openWindow(self):
        '''mở result window khi click search by lyric'''
        global query
        query=self.myTextEdit.toPlainText()
        global check
        check=1
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_result_window()
        self.ui.setupUi(self.window)
        self.window.show()

    def openWindow1(self):
        '''mở result window khi click search by name'''
        global query
        query=self.myTextEdit.toPlainText()
        global check
        check=2
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_result_window()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, Form):
        Form.setObjectName("Music Search Engine")
        Form.resize(972, 552)
        self.myButton = QtWidgets.QPushButton(Form)
        self.myButton.setGeometry(QtCore.QRect(260, 360, 150, 41))
        self.myButton1 = QtWidgets.QPushButton(Form)
        self.myButton1.setGeometry(QtCore.QRect(590, 360, 150, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.myButton.setFont(font)
        self.myButton.setObjectName("myButton")
        self.myButton1.setFont(font)
        self.myButton1.setObjectName("myButton1")
        self.myTextEdit = QtWidgets.QTextEdit(Form)
        self.myTextEdit.setGeometry(QtCore.QRect(260, 290, 481, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.myTextEdit.setFont(font)
        self.myTextEdit.setObjectName("myTextEdit")
        self.logo = QtWidgets.QLabel(Form)
        self.logo.setGeometry(QtCore.QRect(200, 130, 591, 101))
        self.logo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.logo.setText("")
        self.logo.setObjectName("logo")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        pixmap = QPixmap('./UI/logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        self.myButton.clicked.connect(self.openWindow)
        self.myButton1.clicked.connect(self.openWindow1)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Music Search", "Music Search"))
        self.myButton.setText(_translate("Form", "SEARCH BY LYRIC"))
        self.myButton1.setText(_translate("Form", "SEARCH BY NAME"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
