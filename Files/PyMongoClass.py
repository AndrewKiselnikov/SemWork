import json
import datetime
import pymongo
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, QCoreApplication, QSettings,Qt
from bson.son import SON
import pprint
import ast
from playsound import playsound

class MongoClass:
    def __init__(self,form = None,window = None):
        self.form = form
        self.window = window
        self.WorkForm, self.WorkWindow = uic.loadUiType("WorkWindow.ui")
        self.Workapp = QApplication([])
        self.Workwindow = self.WorkWindow()
        self.Workform = self.WorkForm()
        self.Workform.setupUi(self.Workwindow)
        self.ConnectionCheck = False
        self.client = None
        self.db = None
        self.PickDB = None
        self.CollectNames = None
        
        
    def addFile(self,path):
        with open(path, "r") as read_file:
            data = json.load(read_file)
        return data
        
    def prints(self,data):
        return pprint.pprint(data)
        
    def InsertData(self):
        playsound('buttonsound.mp3')
        pipeline = self.Workform.insertLine.text()
        arr = json.loads(pipeline)
        print()
        self.PickDB.insert_one(arr).inserted_id
        self.InitTable()
        
    def DeleteData(self):
        playsound('buttonsound.mp3')
        pipeline = self.Workform.delLine.text()
        arr = json.loads(pipeline) 
        self.PickDB.delete_one(arr)
        self.InitTable()
        
    def UpdateData(self):
        playsound('buttonsound.mp3')
        pipeline = self.Workform.updateLine.text()
        filt,data =  pipeline.split(',')
        filt = json.loads(filt)
        data =  json.loads(data) 
        self.PickDB.find_one_and_update(filt,data)
        self.InitTable()
        
    def InsertScript(self):
        playsound('buttonsound.mp3')
        pipeline = self.Workform.scriptLine.text()
        arr = ast.literal_eval(pipeline)
        self.InitTable(self.PickDB.aggregate(arr))
        
    def ListPick(self,text):
        playsound('buttonsound.mp3')
        if text in self.db.list_collection_names():
            self.PickDB = self.db[text]
        if text != "ChooseCollect":
            self.InitTable()
            
    def InitTable(self,Aggr = None):
        if Aggr != None:
            DataTable = list(Aggr)
        else:
            if self.PickDB != None:
                DataTable = list(self.PickDB.find())
        Row = len(DataTable)
        Max_Col = 0
        Headers = []
        print(DataTable)
        for Doc in DataTable:
            print(Doc)
            if isinstance(Doc,dict):
                for Keys in Doc.keys():
                    if Keys not in Headers:
                        Max_Col +=1
                        Headers.append(Keys)
            else:
                if Doc not in Headers:
                        Max_Col +=1
                        Headers.append(Doc)
                    
        self.Workform.tableList.setColumnCount(Max_Col) # Колонки
        self.Workform.tableList.setRowCount(Row) # строки в таблице
        self.Workform.tableList.setHorizontalHeaderLabels(Headers)
        for i in range (Row):
            k = -1
            if isinstance(DataTable[i],dict):
                for Trash, v in DataTable[i].items():
                    k +=1
                    self.Workform.tableList.setItem(i, k, QTableWidgetItem(str(v)))
            else:
                k +=1
                self.Workform.tableList.setItem(i, k, QTableWidgetItem(str(DataTable[i])))
        self.Workform.tableList.resizeColumnsToContents()
        
    def WorkWithTable(self,item):
        res = item.text() 
        print(res[0])
        print(res[-1])
        #Лучше обработчика я не придумал, что есть то есть
        res = res.replace("'",'"')
        res = res.replace(": d",':"d')
        res = res.replace("),",')",')
        res = res.replace(": O",': "O')
        res = res.replace('("',"('")
        res = res.replace('")',"')")
                    
        if (res[0] !="[") and (res[-1] !="]"):
            res = "[" + res + "]"
        print("Res:",res)
        self.InitTable(json.loads(res))
        
    
    def EnterSys(self):
            self.client = pymongo.MongoClient("mongodb+srv://" + self.form.log.text() + ":" + self.form.password.text() + "@pow1.vsjlf.mongodb.net/SportBD?retryWrites=true&w=majority")
            self.db = self.client.SportBD
            try:
                self.Workform.comboList.addItems(["ChooseCollect"] + self.db.list_collection_names())
                print("Подключенно")
                self.ConnectionCheck = True
                #Тут типа проверка на вход:
            except Exception as e:
                print("Ошибка подключения")
            
        
            self.window.close()
            self.Workwindow.show()
            self.Workform.tableList.itemDoubleClicked.connect(self.WorkWithTable)
            self.Workform.scriptButton.clicked.connect(self.InsertScript)
            self.Workform.insertButton.clicked.connect(self.InsertData)
            self.Workform.updateButton.clicked.connect(self.UpdateData)
            self.Workform.delButton.clicked.connect(self.DeleteData)
            self.Workform.comboList.activated[str].connect(self.ListPick)

            self.Workapp.exec_()
