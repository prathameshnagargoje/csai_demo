import wpf
from checkEncryption import *
from System.Windows import *
from System.Windows.Controls import Button,Grid
from System.Windows.Media import Brushes,Color,ColorConverter,SolidColorBrush
from System import TimeSpan
from System.Windows.Media.Animation import *
import os
import json
from datetime import date,datetime
from LoadingWindow import LoadingWindow
import sys
import subprocess
import re
from threading import Thread
from WindowPDF import WindowPDF

class ServiceCustomer(Window):

    key = ""
    custDict = {'tot_rows':0}
    data_cc=0
    current_data_no=0
    sortByMonth = False
    prev_label_text = ""
    filename = ""

    def windowClosed(self,sender,e):
        del self.custDict
        del self

    def __init__(selfCust,key,filename=""):
        wpf.LoadComponent(selfCust, 'ServiceCustomer.xaml')
        selfCust.key = key
        selfCust.dateDate.SelectedDate = date.today()
        selfCust.showDataGrid.Visibility = Visibility.Hidden
        selfCust.custDeleteGrid.Visibility=Visibility.Hidden
        selfCust.custDict = {'tot_rows':0}
        selfCust.data_cc=0
        selfCust.current_data_no=0
        selfCust.refreshStack()
        selfCust.prev_label_text = ""
        selfCust.custNameText.Text = ""
        selfCust.phoneNoText.Text = ""
        selfCust.placeText.Text = ""
        selfCust.rateText.Text = ""
        selfCust.totRemBalLabel.Content = "00"
        if id(str(filename).strip())!=id(""):
            data_dict = {}
            with open("service_cust\\{}".format(str(filename))) as fp:
                data_dict = json.load(fp)
            selfCust.filename = filename
            if "cust_name" in data_dict.keys():
                selfCust.custNameText.Text = str(data_dict['cust_name']).strip()
            else:
                selfCust.custNameText.Text = ""
            if "phone_no" in data_dict.keys():
                selfCust.phoneNoText.Text = str(data_dict['phone_no']).strip()
            else:
                selfCust.phoneNoText.Text = ""
            if "place" in data_dict.keys():
                selfCust.placeText.Text = str(data_dict['place']).strip()
            else:
                selfCust.placeText.Text = ""
            if "total_rembal" in data_dict.keys():
                selfCust.totRemBalLabel.Content = str(data_dict['total_rembal']).strip()
            else:
                selfCust.totRemBalLabel.Content = ""
            if "tot_rows" in data_dict.keys():
                tot_rows = data_dict['tot_rows']
                if int(tot_rows)>0:
                    for i in range(int(tot_rows)):
                        if str(i) in data_dict.keys():
                            data_dict[i] = data_dict[str(i)]
                            del data_dict[str(i)]
                    selfCust.custDict = data_dict
                    if 0 in data_dict.keys() or str(0) in data_dict.keys():
                        selfCust.refreshStack()

    def ifEnterHit(self,sender,e):
        try:
            if str(e.Key).strip() == "Return":
                if len(str(self.billText.Text).strip())>0 and len(str(self.depositText.Text).strip())>0:
                    self.insertData(None,None)
        except:
            pass
        
    def updateBill(self,sender,e):
        weight=1
        rate = 1
        if str(sender.Name) == "weightText" or str(sender.Name) == "rateText":
            try:
                weight = float(str(self.weightText.Text).strip())
                rate = float(str(self.rateText.Text).strip())
                bill = weight * rate
                self.billText.Text = "{:.2f}".format(bill)
            except:
                pass

    def updateTotRembalLabel(self):
        self.totRemBalLabel.Content=""
        rembal=0.0
        data_cc = int(self.custDict['tot_rows'])
        for i in range(data_cc):
            data = self.custDict[i]
            if "rembal" in data.keys():
                if id(str(data['rembal']).strip())!=id(""):
                    try:
                        rembal+=float(data['rembal'])
                    except:
                        pass
        try:
            self.totRemBalLabel.Content = "{:.2f}".format(float(rembal))
        except:
            pass

    def addNewData(self,sender,e):
        self.custDeleteGrid.Visibility = Visibility.Hidden
        newBtn = Button()
        self.data_cc = int(self.custDict['tot_rows'])
        newBtn.Content = str(self.data_cc+1)
        newBtn.Name = "data_"+str(self.data_cc)
        newBtn.Height = 0
        newBtn.Width = 100
        newBtn.Margin = Thickness(3, 0, 3, 3)
        newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        newBtn.FontSize = 18
        newBtn.Click += self.showData
        newBtn.MouseEnter+=self.dataBtn_MouseEntered
        newBtn.MouseLeave+= self.dataBtn_MouseLeave
        setattr(self,"btn_"+str(self.data_cc),newBtn)
        self.custData_stack.Children.Add(newBtn)
        self.custDict[self.data_cc] = {'date':str(self.dateDate.SelectedDate).split(' ')[0],'weight':0.0,'rate':0,'bill':0,'deposit':0,'rembal':0}
        self.showDataGrid.Visibility = Visibility.Hidden
        self.data_cc+=1
        self.custDict['tot_rows']=self.data_cc
        da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
        newBtn.BeginAnimation(Button.HeightProperty,da)

    def showData(self,sender,e):
        try:
            data_no = int(str(sender.Name).split("_")[1])
            self.showDataLabel.Content = str(data_no+1)
            self.custDeleteGrid.Visibility = Visibility.Hidden
            self.current_data_no=data_no
            data = {}
            if data_no in self.custDict.keys():
                data = self.custDict[data_no]
            else:
                data = self.custDict[str(data_no)]
            self.dateDate.SelectedDate = datetime.strptime(data['date'],'%d-%m-%Y')

            if id(str(data['weight']).strip())!=id(""):
                if float(data['weight'])>0:
                    self.weightText.Text = str(data['weight'])
                else:
                    self.weightText.Text = ''
            else:
                self.weightText.Text = ''
            try:
                if id(str(data['rate']).strip())!=id(""):
                    if float(data['rate'])>0:
                        self.rateText.Text = str(data['rate'])
                    else:
                        self.rateText.Text = ''
                else:
                    self.rateText.Text = ''
            except:
                self.rateText.Text = ''
            if id(str(data['bill']).strip())!=id(""):
                if float(data['bill'])>=0:
                    self.billText.Text = str(data['bill'])
                else:
                    self.billText.Text = ''
            else:
                self.billText.Text = ''
            if id(str(data['deposit']).strip())!=id(""):
                if float(data['deposit'])>=0:
                    self.depositText.Text = str(data['deposit'])
                else:
                    self.depositText.Text = ''
            else:
                self.depositText.Text = ''
            if id(str(data['rembal']).strip())!=id(""):
                self.remBalText.Text = str(data['rembal'])
            else:
                self.remBalText.Text = ''
            
            self.showDataGrid.Opacity = 0
            self.showDataGrid.Visibility = Visibility.Visible
            da = DoubleAnimation(1,TimeSpan.FromMilliseconds(200))
            self.showDataGrid.BeginAnimation(Grid.OpacityProperty,da)
        except Exception as e:
            print(e)


    def refreshStack(self):
        while self.custData_stack.Children.Count>0:
            self.custData_stack.Children.RemoveAt(self.custData_stack.Children.Count-1)
        data_cc = int(self.custDict['tot_rows'])
        if data_cc>0:
            for i in range(data_cc):
                newBtn = Button()
                data = {}
                if i in self.custDict.keys():
                    data = self.custDict[i]
                else:
                    data = self.custDict[str(i)]
                newBtn.Content = str(i+1)
                newBtn.Name = "data_"+str(i)
                newBtn.Height = 0
                newBtn.Width = 100
                newBtn.Margin = Thickness(3, 0, 3, 3)
                newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.FontSize = 18
                newBtn.Click += self.showData
                newBtn.MouseEnter+=self.dataBtn_MouseEntered
                newBtn.MouseLeave+= self.dataBtn_MouseLeave
                setattr(self,"btn_"+str(i),newBtn)
                self.custData_stack.Children.Add(newBtn)
                self.showDataGrid.Visibility = Visibility.Hidden
                da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                newBtn.BeginAnimation(Button.HeightProperty,da)


    def sortByDate(self,sender,e):
        self.showDataGrid.Visibility = Visibility.Hidden
        temp = []
        for i in range(int(self.custDict['tot_rows'])):
            temp.append(self.custDict[i])
        temp.sort(key=lambda x: datetime.strptime(x['date'],'%d-%m-%Y'))
        for i in range(0,len(temp)):
            self.custDict[i]=temp[i]
        self.refreshStack()

    def updateRemBalText(self,sender,e):
        bill = str(self.billText.Text).strip()
        deposit=str(self.depositText.Text).strip()
        try:
            if id(bill)!=id("") and id(deposit)!=id(""):
                self.remBalText.Text = "{:.2f}".format(float(bill)-float(deposit))
            else:
                self.remBalText.Text = ""
        except:
            self.remBalText.Text = ""

    def dataBtn_MouseLeave(self,sender,e):
        data_no = int(str(sender.Name).split("_")[1])
        sender.Content = str(data_no+1)
        da = DoubleAnimation(100,TimeSpan.FromMilliseconds(200))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BeginAnimation(Button.WidthProperty,da)

    def dataBtn_MouseEntered(self,sender,e):
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        try:
            data_no = int(str(sender.Name).split("_")[1])
            self.prev_label_text = str(sender.Content)
            if data_no in self.custDict.keys():
                data = self.custDict[data_no]
            else:
                data = self.custDict[str(data_no)]
            da = DoubleAnimation(270,TimeSpan.FromMilliseconds(200))
            sender.BeginAnimation(Button.WidthProperty,da)
            try:
                if id(str(data['bill']).strip())!=id(""):
                    if float(data['bill'])>0:
                        bill = "{:.0f}".format(float(data['bill']))
                    else:
                        bill = "0"
                else:
                    bill = ""
                if id(str(data['rembal']).strip())!=id(""):
                    if float(data['rembal'])>0:
                        rembal= "{:.0f}".format(float(data['rembal']))
                    else:
                        rembal=""
                else:
                    rembal=""
                if id(str(bill).strip())!=id("") and id(str(rembal).strip())!=id(""):
                    sender.Content = "(bill: {}, rem: {})".format(bill,rembal)
                elif id(str(bill).strip())!=id(""):
                    sender.Content = "(bill: {})".format(bill)
                elif id(str(rembal).strip())!=id(""):
                    sender.Content = "(rem: {})".format(rembal)
                else:
                    sender.Content = "Empty"
            except:
                sender.Content = "Empty"
        except:
            pass


    def insertData(self,sender,e):
        data_no = self.current_data_no
        data = self.custDict[data_no]
        flag = True
        self.updateRemBalText(sender,e)
        try:
            if id(str(self.weightText.Text).strip())!=id(""):
                _=float(str(self.weightText.Text).strip())
        except:
            self.weightText.Text = ""
            flag=False
        try:
            if id(str(self.rateText.Text).strip())!=id(""):
                _=float(str(self.rateText.Text).strip())
        except:
            self.rateText.Text = ""
            flag=False
        try:
            if id(str(self.billText.Text).strip())!=id(""):
                _=float(str(self.billText.Text).strip())
        except:
            flag=False
            self.billText.Text = ""
        try:
            if id(str(self.depositText.Text).strip())!=id(""):
                _=float(str(self.depositText.Text).strip())
        except:
            flag=False
            self.depositText.Text = ""
        try:
            if id(str(self.remBalText.Text).strip())!=id(""):
                _=float(str(self.remBalText.Text).strip())
        except:
            flag=False
            self.weightText.Text = ""
        if flag:
            data['date']=str(self.dateDate.SelectedDate).split(' ')[0]
            data['weight']=str(self.weightText.Text).strip()
            data['rate'] = str(self.rateText.Text).strip()
            data['bill']=str(self.billText.Text).strip()
            data['deposit']=str(self.depositText.Text).strip()
            data['rembal']=str(self.remBalText.Text).strip()
            self.showDataGrid.Visibility = Visibility.Hidden
            self.updateTotRembalLabel()
        else:
            MessageBox.Show("Data Entered is Unexpected...\nPlese Enter Correct Data...")

    def saveFinalData(self,sender,e):
        try:
            custName = str(self.custNameText.Text).strip()
            data = self.custDict
            data['cust_name'] = custName
            data['phone_no'] = str(self.phoneNoText.Text).strip()
            data['place'] = str(self.placeText.Text).strip()
            data['length'] = int(data['tot_rows'])
            data['total_rembal'] = str(self.totRemBalLabel.Content).strip()
            date_now = datetime.now().date()
            data['c_month'] = date_now.month
            data['c_year'] = date_now.year
            filename = encrypt(custName,self.key)
            if "filename" in data.keys():
                if str(data['filename']) != filename:
                    filename = str(data['filename'])
            elif self.filename!="":
                if len(self.filename)>0:
                    filename = str(self.filename).split('.csai')[0]
            data['filename'] = filename
            file_path = "service_cust/"+filename+".csai"
            if not os.path.isdir('service_cust'):
                os.makedirs('service_cust')
            with open(file_path, 'w') as fp:
                json.dump(data, fp)
            sync_data = "service_cust\t"+filename+"\n"
            with open("sync_list.csai",'a') as fp:
                fp.write(sync_data)
            MessageBox.Show("Service Customer Data has been saved...")
            self.Close()
        except:
            MessageBox.Show("Error: Input Data is not as expected...")

    def genPDF_Click(self,sender,e):
        try:
            custName = str(self.custNameText.Text).strip()
            data = self.custDict
            data['cust_name'] = custName
            data['phone_no'] = str(self.phoneNoText.Text).strip()
            data['place'] = str(self.placeText.Text).strip()
            data['length'] = int(data['tot_rows'])
            data['total_rembal'] = str(self.totRemBalLabel.Content).strip()
            date_now = datetime.now().date()
            data['c_month'] = date_now.month
            data['c_year'] = date_now.year
            filename = encrypt(custName,self.key)
            if "filename" in data.keys():
                if str(data['filename']) != filename:
                    filename = str(data['filename'])
            elif self.filename!="":
                if len(self.filename)>0:
                    filename = str(self.filename).split('.csai')[0]
            data['filename'] = filename
            file_path = "service_cust/"+filename+".csai"
            if not os.path.isdir('service_cust'):
                os.makedirs('service_cust')
            with open(file_path, 'w') as fp:
                json.dump(data, fp)
            sync_data = "service_cust\t"+filename+"\n"
            with open("sync_list.csai",'a') as fp:
                fp.write(sync_data)
            loadingWindow = LoadingWindow()
            loadingWindow.Show()
            self.Hide()
            args = ['ppython/python.exe', 'customerPDF.py', 'service_cust/{}'.format(filename)]
            process = run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                if int(process[0])==1:
                    self.Show()
                    loadingWindow.Close()
                    MessageBox.Show("Error while genrating PDF...\n\n{}".format(str(process)))
                elif int(process[0])==0:
                    form = WindowPDF()
                    form.Show()
                    self.Close()
                    loadingWindow.Close()
                    del loadingWindow
                else:
                    print("Got something else...")
                    print(str(process))
            except:
                MessageBox.Show("Error")
        except:
            MessageBox.Show("Error: Input Data is not as expected...")
        

    def showDeleteDataGrid(self,sender,e):
        self.deleteComboBox.Items.Clear()
        for i in range(int(self.custDict['tot_rows'])):
            self.deleteComboBox.Items.Add(str(i+1))
        self.showDataGrid.Visibility = Visibility.Hidden
        self.custDeleteGrid.Visibility=Visibility.Visible

    def button_MouseEnter(self,sender,e):
        if str(sender.Content).strip() == "X":
            sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE21C17"))
        else:
            sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF2D3436"))

    def button_MouseLeave(self,sender,e):
        if str(sender.Content).strip()=="X":
            sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE21C17"))
        else:
            sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))

    def deleteCustomer_Click(self,sender,e):
        filename = self.filename.split(".csai")[0]
        if filename == "":
            file_path = ""
            if 'cust_name' in self.custDict.keys():
                custName = self.custDict['cust_name']
                filename = encrypt(custName,self.key)
                file_path = "service_cust/"+filename+".csai"
            else:
                custName = str(self.custNameText.Text).strip()
                filename = encrypt(custName,self.key)
                file_path = "service_cust/"+filename+".csai"
        else:
            file_path = "service_cust/"+filename+".csai"
        if file_path!="":
            try:
                os.remove(file_path)
                with open("sync_list.csai",'a')as fp:
                    fp.write("del\tservice_cust\t{}\n".format(filename))
            except:
                pass
        self.Close()
        MessageBox.Show("Please update current status to Cloud Database...\n By clicking UPLOAD button...")

    def deleteData_Click(self,sender,e):
        try:
            data_no = str(self.deleteComboBox.SelectedValue)
            data_no = int(data_no)-1
            for i in range(int(self.custDict['tot_rows'])):
                if i==data_no:
                    if i in self.custDict.keys():
                        del self.custDict[i]
                if i>data_no:
                    if i in self.custDict.keys():
                        self.custDict[i-1]=self.custDict[i]
                        del self.custDict[i]
            self.custDeleteGrid.Visibility = Visibility.Hidden
            data_cc = int(self.custDict['tot_rows'])
            self.custDict['tot_rows'] = data_cc-1
            self.refreshStack()
            self.updateTotRembalLabel()
        except:
            MessageBox.Show("Error while deleting selected Data...")

def run(*popenargs, **kwargs):
    input = kwargs.pop("input", None)
    check = kwargs.pop("handle", False)

    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr