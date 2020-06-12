import kivy
import sqlite3
from datetime import date,datetime
from kivy.app import App
from kivy .uix.screenmanager import  ScreenManager,Screen,SlideTransition
from kivy.uix.button import Button
from kivy.uix.gridlayout import  GridLayout
from kivy.uix.boxlayout import  BoxLayout
from kivy.uix.label import  Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import  Popup
from kivy.uix.scrollview import ScrollView
from prettytable import PrettyTable

tableview = PrettyTable()
tableData = ''
heading = Label(text='Jagdamba Saree Palace',font_size = 30,color=[212,175,55,1])
heading.pos_hint= {'x': 0.01, 'y': 0.4}
Window.add_widget(heading)

popup = Popup(title='Invalid Input',
    content=Label(text='TRY Again!!!!',color=[1,0,0,1]),
    size_hint=(None, None), size=(200, 200))

list_popup = Popup(title='Invalid Input',
    content=Label(text=tableData,color=[1,1,1,1]),
    size_hint=(None, None), size=(400, 400))
menu_label = Label(text='Menu', font_size=30,opacity = 0)
menu_label.pos_hint = {'x': 0.01, 'y': 0.4}
Window.add_widget(menu_label)

cal_label = Label(text='Calculate Saree No', font_size=30,opacity = 0)
cal_label.pos_hint = {'x': 0.01, 'y': 0.4}
Window.add_widget(cal_label)

scroll_label = Label(text='Available List', font_size=30,opacity = 0)
scroll_label.pos_hint = {'x': 0.01, 'y': 0.4}
Window.add_widget(scroll_label)

create_label = Label(text='Create List', font_size=30,opacity = 0)
create_label.pos_hint = {'x': 0.01, 'y': 0.4}
Window.add_widget(create_label)

sm = ScreenManager(transition=SlideTransition())
s6 = None
s5 = None
s4 = None
s3 = None
s2 = None
database = None
database2 = None
gst = 0
factor = 0
flag = 4

class Bill:
    def __init__(self,**kwargs):
        self.sareeName = kwargs['sareeName']
        self.costPrice = kwargs['costPrice']
        self.sellingPrice = kwargs['sellingPrice']
        self.sareeNo = kwargs['sareeNo']
        self.date = kwargs['date']
class Database2:
    def __init__(self):
        self.filename = 'record.db'
        self.conn = sqlite3.connect(self.filename)
        self.cur = self.conn.cursor()
        try:
            self.cur.execute('create table tables(tableName text)')
        except:
            pass
    def insertData(self,record):
        query = "INSERT INTO tables values('{}')".format(record)
        try:
            self.cur.execute(query)

        except:
            pass
        self.conn.commit()
    def exportData(self):
        return (self.cur.execute('select * from tables'))
    def deleteAllRecords(self):
        try:
            self.cur.execute('delete from tables')
        except:
            pass

class Database:
    def __init__(self,filename):
        self.filename = filename

        self.conn = sqlite3.connect(self.filename)
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("CREATE TABLE bill(sareeName text,costPrice real,sellingPrice real,sareeNo integer,date text)")
        except:
            pass

    def insertData(self,bill):
        query = "INSERT INTO bill values('{}',{},{},{},'{}')".format(bill.sareeName,bill.costPrice,bill.sellingPrice,bill.sareeNo,str(bill.date))
        try:
            self.cur.execute(query)
            self.conn.commit()
        except:
            pass

    def exportData(self):
        return (self.cur.execute('select * from bill'))


class LoginScreenUi(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreenUi, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 10
        self.size_hint_x = 0.9
        self.size_hint_y = 0.3
        self.pos_hint = {'center_x': 0.4, 'center_y': 0.5}
        self.add_widget(Label(text='User Name :'))
        self.uname =  TextInput(multiline=False,font_size=30)

        self.add_widget(self.uname)
        self.add_widget(Label(text='User Password :'))
        self.password = TextInput(password=True,multiline = False,font_size=30)
        self.add_widget(self.password)
        self.add_widget(Label(text=''))
        self.loginButton = Button(text='SIGN IN', font_size=20,color=[255,215,0,1])
        self.add_widget(self.loginButton)


    def login(self,obj):
        global heading,s2
        if self.uname.text == 'mamta' and self.password.text == 'mamta123':
            menu_label.opacity = 1
            heading.opacity = 0
            sm.switch_to(s2)
        else:
           popup.open()

    def bindAllFunc(self):
        self.loginButton.bind(on_press = self.login)


class MenuScreenUi(GridLayout):
    def __init__(self,**kwargs):
        super(MenuScreenUi,self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 10
        self.size_hint_x = 0.8
        self.size_hint_y = 0.5
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.calNo = Button(text='Calculate Saree Number',font_size=20)
        self.add_widget(self.calNo)
        self.listButton = Button(text='Create List', font_size=20)
        self.add_widget(self.listButton)
        self.viewListButton = Button(text='View List', font_size=20)
        self.add_widget(self.viewListButton)
        self.add_widget(Button(text='B4'))

    def shiftToListScreen(self,obj):
        global flag,database,database2,menu_label,create_label
        flag = 5
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("(%H-%M)")
        filename = '{}-{}.db'.format(today,current_time)
        database = Database(filename)
        database2.insertData(filename)
        menu_label.opacity = 0
        create_label.opacity = 1
        sm.switch_to(s3)

    def viewList(self,obj):
        global menu_label, scroll_label
        menu_label.opacity = 0
        scroll_label.opacity = 1
        sm.switch_to(s6)


    def nextScreen(self,obj):
        menu_label.opacity = 0
        cal_label.opacity = 1
        sm.switch_to(s3)
    def bindAllFunct(self):
        self.calNo.bind(on_press=self.nextScreen)
        self.listButton.bind(on_press=self.shiftToListScreen)
        self.viewListButton.bind(on_press=self.viewList)
class InputScreenUi(GridLayout):
    def __init__(self,**kwargs):
        super(InputScreenUi,self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 10
        self.size_hint_x = 0.9
        self.size_hint_y = 0.3
        self.pos_hint = {'center_x': 0.4, 'center_y': 0.5}
        self.add_widget(Label(text = 'GST :'))
        self.gstinput = TextInput(multiline = False,font_size=30)
        self.add_widget(self.gstinput)
        self.add_widget(Label(text = "Factor :"))
        self.factorinput = TextInput(multiline=False,font_size=30)
        self.add_widget(self.factorinput)
        self.save = Button(text='SAVE',font_size = 20)
        self.add_widget(self.save)
        self.back = Button(text = 'BACK',font_size = 20)
        self.add_widget(self.back)


    def checkInput(self):
        return (self.gstinput.text.isdigit() and self.factorinput.text.isdigit())

    def switchBack(self,obj):
        sm.switch_to(s2)
        menu_label.opacity = 1
        cal_label.opacity = 0
        create_label.opacity = 0

    def saveInput(self,obj):
        global gst,factor,flag
        if self.checkInput():
            gst = self.gstinput.text
            factor = self.factorinput.text
            if flag == 4:
                sm.switch_to(s4)
            elif flag == 5:
                sm.switch_to(s5)

        else:
            popup.open()

    def bindAllFunct(self):
        self.back.bind(on_press=self.switchBack)
        self.save.bind(on_press = self.saveInput)

class CalculatorUi(GridLayout):
    def __init__(self,**kwargs):
        super(CalculatorUi,self).__init__(**kwargs)
        self.cols = 1
        self.spacing = 5
        self.size_hint_x = 0.8
        self.size_hint_y = 0.5
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(Label(text='Enter Price Of Saree'))
        self.cpinput = TextInput(multiline=False,font_size=30,text='0')
        self.add_widget(self.cpinput)
        self.ansLabel = Label(text = "0",color=[0,1,0,1],font_size=30)
        self.add_widget(self.ansLabel)
        self.backButton = Button(text='Back')
        self.add_widget(self.backButton)

    def calSareeNo(self,obj,obj2):
        global gst,factor
        try:
            temp_cp = float(self.cpinput.text)
            temp_gst = int(gst)
            temp_factor = int(factor)
            self.my_cp = str(temp_cp + ((temp_gst/100.0) * temp_cp))
            myList = self.my_cp.split('.')
            if int(myList[1][0:2]) > 50:
                self.my_cp = int(myList[0]) + 1
            else:
                self.my_cp = int(myList[0])
            self.result = self.my_cp * temp_factor
            self.ansLabel.text = str(self.result)
        except:
            self.ansLabel.text = '0'

    def switchBack(self,obj):
        sm.switch_to(s3)

    def bindAllFunc(self):
        self.backButton.bind(on_press = self.switchBack)
        self.cpinput.bind(text=self.calSareeNo)

class ListScreenUi(GridLayout):
    def __init__(self,**kwargs):
        super(ListScreenUi,self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 10
        self.size_hint_x = 0.9
        self.size_hint_y = 0.3
        self.pos_hint = {'center_x': 0.4, 'center_y': 0.5}
        self.add_widget(Label(text='Saree Name :'))
        self.nameInput = TextInput(multiline=False, font_size=30)
        self.add_widget(self.nameInput)
        self.add_widget(Label(text="Cost Price :"))
        self.priceInput = TextInput(multiline=False, font_size=30)
        self.add_widget(self.priceInput)
        self.done = Button(text='DONE', font_size=20)
        self.add_widget(self.done)
        self.next = Button(text='NEXT', font_size=20)
        self.add_widget(self.next)

    def switchBack(self,obj):
        global flag,database,menu_label,create_label
        menu_label.opacity = 1
        create_label.opacity = 0
        flag = 4
        sm.switch_to(s2)
    def calSareeNo(self):
        temp_cp = float(self.price)
        temp_gst = int(gst)
        temp_factor = int(factor)
        self.my_cp = str(temp_cp + ((temp_gst / 100.0) * temp_cp))
        myList = self.my_cp.split('.')
        if int(myList[1][0:2]) > 50:
            self.my_cp = int(myList[0]) + 1
        else:
            self.my_cp = int(myList[0])
        self.result = self.my_cp * temp_factor

    def getObject(self):
        self.todayDate = date.today()
        self.name = self.nameInput.text
        self.price = float(self.priceInput.text)
        self.calSareeNo()
        record = Bill(sareeName=self.name,costPrice=self.price,sellingPrice=float(self.my_cp),sareeNo=self.result,date=self.todayDate)
        return record
    def saveToDatabase(self,obj):
        global database
        record = self.getObject()
        database.insertData(record)
        self.nameInput.text = ''
        self.priceInput.text = ''
    def bindAllfunction(self):
        self.done.bind(on_press=self.switchBack)
        self.next.bind(on_press=self.saveToDatabase)


class SliderScreenUi(ScrollView):
    def __init__(self,**kwargs):
        global database2
        super(SliderScreenUi,self).__init__(**kwargs)
        self.size_hint_x = 0.8
        self.size_hint_y = 0.8
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        self.scroll_timeout = 250
        self.scroll_distance = 20
        self.layout = GridLayout(cols = 1,spacing = 5,size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.back = Button(text='BACK', size_hint_y=None,color=[0,1,0,1])
        self.layout.add_widget(self.back)
        self.add_widget(self.layout)

    def display(self,obj):
        global tableview,tableData
        filename = obj.text
        try:
            self.db = Database(filename)
        except:
            pass
        data = self.db.exportData()
        tableview.field_names = ['Saree Name','Cp','Sp','SareeNo','Date']
        for tuple in data:
            tableview.add_row(list(tuple))
        print(tableview)
    def backToMenu(self,obj):
        global scroll_label,menu_label
        menu_label.opacity = 1
        scroll_label.opacity = 0
        sm.switch_to(s2)
    def bindAllFunct(self):
        self.back.bind(on_press=self.backToMenu)

class LoginScreen(Screen):
    def __init__(self,**kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        self.ui = LoginScreenUi()
        self.ui.bindAllFunc()
        self.add_widget(self.ui)

class MenuScreen(Screen):
    def __init__(self,**kwargs):
        super(MenuScreen,self).__init__(**kwargs)
        self.menu_ui = MenuScreenUi()
        self.add_widget(self.menu_ui)
        self.menu_ui.bindAllFunct()

class InputScreen(Screen):
    def __init__(self,**kwargs):
        super(InputScreen,self).__init__(**kwargs)
        self.input_ui = InputScreenUi()
        self.add_widget(self.input_ui)
        self.input_ui.bindAllFunct()
class CalculatorScreen(Screen):
    def __init__(self,**kwargs):
        super(CalculatorScreen,self).__init__(**kwargs)
        self.calculatorui = CalculatorUi()
        self.add_widget(self.calculatorui)
        self.calculatorui.bindAllFunc()
class ListScreen(Screen):
    def __init__(self,**kwargs):
        super(ListScreen,self).__init__(**kwargs)
        self.listui = ListScreenUi()
        self.add_widget(self.listui)
        self.listui.bindAllfunction()
class SliderScreen(Screen):
    def __init__(self,**kwargs):
        super(SliderScreen,self).__init__(**kwargs)
        self.sliderui = SliderScreenUi()
        self.sliderui.bindAllFunct()
        self.add_widget(self.sliderui)

    def on_enter(self, *args):
        self.sliderui.layout.add_widget(self.sliderui.back)
        for buttonText in database2.exportData():
             for i in buttonText:
                 print(i)
                 self.sliderui.layout.add_widget(Button(text=i, size_hint_y=None,height=80,on_press=self.sliderui.display,font_size=20))
    def on_pre_enter(self, *args):
        self.sliderui.layout.clear_widgets()

class TestApp(App):

    def build(self):
        global s3,s2,s4,s5,s6
        self.title = 'Manage Saree'

        try:
            global database2
            database2 = Database2()
        except:
            pass

        sm.add_widget(LoginScreen(name ='login'))
        s2 = MenuScreen(name='menu')
        sm.add_widget(s2)
        s3 = InputScreen(name='input')
        sm.add_widget(s3)
        s4 = CalculatorScreen(name='calculator')
        sm.add_widget(s4)
        s5 = ListScreen(name='list')
        sm.add_widget(s5)
        s6 = SliderScreen(name='slider')
        sm.add_widget(s6)
        return sm

if __name__ == '__main__':
    TestApp().run()
    if database is not None:
        database.conn.close()
        database2.conn.close()

