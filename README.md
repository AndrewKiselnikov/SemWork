# Описание разметки файла README.md
Для описания проектов на GitHub используется README.md, который пишется на языке разметки markdown. Что и как поддерживается расписано ниже. Также существует еще один формат - [reStructuredText](https://github.com/GnuriaN/format-README/blob/master/README.rst), описание которого вынесено в отдельный файл `README.rst`.

## Оглавление

0. [О проекте](#О-проекте)
1. [Инструкция](#Инструкция)
2. [Окно входа](#Окно-входа)
    1. [Информация по коду с окном входа](##Информация-по-коду-с-окном-входа)
3. [Окно для работы с базой данных](#Окно-для-работы-с-базой-данных)
    1. [Информация по коду с окном для работы с базой данных](##Информация-по-коду-с-окном-для-работы-с-базой-данных)

    
# О проекте
Мы создали приложение для входа в нашу документоориентированную СУБД MongoDB.Наше приложение позволяет получать документы напрямую из БД.
А так же мы можем дополнять,удалять и изменять данные прямо из нашего приложения

# Инструкция
Скачать и запустить .exe файл (???) Profit!
Или скачать архив и запустить MainSemWork.py

# Окно входа
[*Клик*](https://raw.githubusercontent.com/AndrewKiselnikov/SemWork/main/optional/Login_ui.PNG "Окно входа")
____
Это окно входа куда нужно ввести пароль и логин, для подключения к нашей БД
Так же если необходимо можно запомнить логин и пароль(Сохранение происходит в реестре)
## Информация по коду с окном входа
Функция "save_widgets"
```
def save_widgets():
    settings = QSettings()
    settings.setValue('log',form.log.text())
    settings.setValue('pass',form.password.text())
    settings.sync()
```
Отвечает за сохранение настроек, настройки сохранения описанные выше по коду,а ниже этой функции идёт считывание

А функция вызываемое нажатием клавишей Acc.EnterSys
```
form.LogButton.clicked.connect(Acc.EnterSys)
```
Отвечает за переход к новому файлу и окну для работы с БД
 
# Окно для работы с базой данных
[*Клик*](https://github.com/AndrewKiselnikov/SemWork/blob/main/optional/Work_ui.png?raw=true "Окно для работы с БД")
____
Это окно для работы с БД,в правом верхнем углу мы выбираем коллекцию, далее она отображается в нашей табличке
Так же мы можем изменять данные в БД и делать к ней запросы (Всё выполняется в синтаксисе JS)
Для расскрытия вложенностей следует нажать двойным кликом на ячейку
## Информация по коду с окном для работы с базой данных
Метод __init__ Это обычная иницилизация,ничего интересного
```
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
```
Методы addFile и prints нужны были для отладки и DragAndDrop( Которого нет :D, на этом всё )

Метод InsertData
Вставляет наши данные в коллекцию на вход подаём строку в стиле JS

```
    def InsertData(self):
        playsound('buttonsound.mp3')
        pipeline = self.Workform.insertLine.text()
        arr = json.loads(pipeline)
        print()
        self.PickDB.insert_one(arr).inserted_id
        self.InitTable()
```
Метод DeleteData
Удаляет наши данные в коллекцию на вход подаём строку в стиле JS
```
    def DeleteData(self):
        playsound('buttonsound.mp3')
        pipeline = self.Workform.delLine.text()
        arr = json.loads(pipeline) 
        self.PickDB.delete_one(arr)
        self.InitTable()
```

Метод UpdateData
Обновляет наши данные в коллекцию на вход подаём строку в стиле JS где есть фильтр, а так же данные которые нужно изменить
```
    def UpdateData(self):
        playsound('buttonsound.mp3')
        pipeline = self.Workform.updateLine.text()
        filt,data =  pipeline.split(',')
        filt = json.loads(filt)
        data =  json.loads(data) 
        self.PickDB.find_one_and_update(filt,data)
        self.InitTable()
```

Метод InsertScript
Выполняет агрегационный скрипт в нашей коллекции на вход подаём строку в стиле JS в синтаксисе MongoDB
```
    def InsertScript(self):
        playsound('buttonsound.mp3')
        pipeline = self.Workform.scriptLine.text()
        arr = ast.literal_eval(pipeline)
        self.InitTable(self.PickDB.aggregate(arr))
```
Метод ListPick
Позволяет выбрать коллекции в нашей БД
```
    def ListPick(self,text):
        playsound('buttonsound.mp3')
        if text in self.db.list_collection_names():
            self.PickDB = self.db[text]
        if text != "ChooseCollect":
            self.InitTable()
```
Иницилизация таблицы, важный и сложный компонент. Показывает данные в нашей таблице,вызывается каждый раз при работе с данными
Метод InitTable

```
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
```
Метод WorkWithTable
Обрабатывает вложенности в коллекции, и создаёт новую таблицу при двойном клике

```
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
```
Метод EnterSys
Проверка на подключение к MongoDB, а так же пул обработчиков после успешного входа
```
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
```
