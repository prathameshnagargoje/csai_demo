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
from calendar import monthrange
import random
import string
import sys
import subprocess
import re
from threading import Thread
from LoadingWindow import LoadingWindow
from WindowPDF import WindowPDF


class ContractorWindow(Window):

    key = ""
    month = ['--Select--','Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
    contractorDict = {}
    current_day = 0

    def __init__(selfContractor,key):
        selfContractor.key = key
        selfContractor.contractorDict = {}
        selfContractor.current_day = 0
        wpf.LoadComponent(selfContractor, 'ContractorWindow.xaml')
        selfContractor.dataGrid.Visibility = Visibility.Hidden
        selfContractor.dateStackGrid.Visibility = Visibility.Hidden
        for i in range(0,len(selfContractor.month)):
            selfContractor.monthComboBox.Items.Add(str(selfContractor.month[i]))
        selfContractor.monthComboBox.SelectedValue = str(selfContractor.month[0])
        selfContractor.yearComboBox.Items.Add("--Select--")
        current_year = int(str(datetime.now().year).strip())
        for i in range(2020,current_year+1):
            selfContractor.yearComboBox.Items.Add(str(i))
        selfContractor.yearComboBox.SelectedValue = str("--Select--")
        selfContractor.totalAdvanceLabel.Content = "0"
        selfContractor.totalWeightLabel.Content = "0"

    def comboSelected(self,sender,e):
        month = str(self.monthComboBox.SelectedValue).strip()
        year = str(self.yearComboBox.SelectedValue).strip()
        if month!='--Select--' and year!='--Select--':
            if month in self.month:
                self.getData_Click(None,None)

    def button_MouseEnter(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF2D3436"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))

    def button_MouseLeave(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))

    def getData_Click(self,sender,e):
        month = str(self.monthComboBox.SelectedValue).strip()
        self.dataGrid.Visibility = Visibility.Hidden
        self.dateStackGrid.Opacity = 0
        self.dateStackGrid.Visibility = Visibility.Visible
        da = DoubleAnimation(1,TimeSpan.FromMilliseconds(200))
        self.dateStackGrid.BeginAnimation(Grid.OpacityProperty,da)
        year = str(self.yearComboBox.SelectedValue).strip()
        self.contractorDict['month']=month
        self.contractorDict['year']=year
        if id(month)!=id(str("--Select--")) and id(year)!=id(str("--Select--")):
            try:
                filename = encrypt("{}_{}".format(month,year),self.key)
                path = "contractor/{}.csai".format(filename)
                if os.path.isfile(path):
                    with open(path,'r') as fp:
                        self.contractorDict = json.load(fp)
                    for i in range(int(self.contractorDict['total_rows'])):
                        if i in self.contractorDict.keys():
                            continue
                        if str(i) in self.contractorDict.keys():
                            self.contractorDict[i]=self.contractorDict[str(i)]
                            del self.contractorDict[str(i)]
                    if "contractor_name" in self.contractorDict.keys():
                        self.contractorNameText.Text = str(self.contractorDict['contractor_name'])
                    if "phone_no" in self.contractorDict.keys():
                        self.phoneNoText.Text = str(self.contractorDict['phone_no'])
                    if "team_of" in self.contractorDict.keys():
                        self.teamOfText.Text = str(self.contractorDict['team_of'])
                    if "rate" in self.contractorDict.keys():
                        self.rateText.Text = str(self.contractorDict['rate'])
                    if "total_advance" in self.contractorDict.keys():
                        self.totalAdvanceLabel.Content = str(self.contractorDict['total_advance'])
                    else:
                        self.totalAdvanceLabel.Content = "0"
                    if "total_weight" in self.contractorDict.keys():
                        self.totalWeightLabel.Content = str(self.contractorDict['total_weight'])
                    else:
                        self.totalWeightLabel.Content = "0"
                    if not "filename" in self.contractorDict.keys():
                        self.contractorDict['filename'] = filename

                days = monthrange(int(year),self.month.index(str(month)))
                self.contractorDict['total_rows'] = int(days[1])
                for i in range(int(days[1])):
                    newBtn = Button()
                    newBtn.Content = str(i+1)
                    newBtn.Name = "dayBtn_"+str(i)
                    newBtn.Height = 0
                    newBtn.Width = 100
                    newBtn.Margin = Thickness(3, 0, 3, 3)
                    newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                    newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                    newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                    newBtn.FontSize = 18
                    newBtn.Click += self.dayBtn_Click
                    newBtn.MouseEnter+=self.dayBtn_MouseEnter
                    newBtn.MouseLeave+=self.dayBtn_MouseLeave
                    self.dateStack.Children.Add(newBtn)
                    setattr(self,"dayBtn_"+str(i),newBtn)
                    if not i in self.contractorDict.keys():
                        dateStr = "{} - {} - {}".format(i+1,month,year)
                        self.contractorDict[i] = {'date':'','weight':'', 'cust_name':'',
                                                'advance':'','by_hand':'','description':''}
                    da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                    newBtn.BeginAnimation(Button.HeightProperty,da)
            except:
                self.dateStackGrid.Visibility = Visibility.Hidden
                MessageBox.Show("Please select month and year properly...\n Got Invalid value...")
        else:
            MessageBox.Show("Please select month and year properly...\n Got Invalid value...")
        
    def ifEnterHit(self,sender,e):
        try:
            if str(e.Key).strip() == "Return":
                self.insertBtn_Click(None,None)
        except:
            pass

    
    def dayBtn_Click(self,sender,e):
        month = str(self.monthComboBox.SelectedValue)
        year = str(self.yearComboBox.SelectedValue)
        self.current_day = int(str(sender.Name).split("_")[1])
        day = str(self.current_day+1)
        self.dateLabel.Content = "{} - {} - {}".format(day,month,year)
        try:
            if self.current_day in self.contractorDict.keys():
                data = self.contractorDict[self.current_day]
            else:
                data = self.contractorDict[str(self.current_day)]
            self.weightText.Text = str(data['weight'])
            self.custNameText.Text = str(data['cust_name'])
            self.advanceText.Text = str(data['advance'])
            self.byHandText.Text = str(data['by_hand'])
            self.descriptionText.Text = str(data['description'])
        except:
            pass
        self.dataGrid.Opacity = 0
        self.dataGrid.Visibility = Visibility.Visible
        da = DoubleAnimation(1,TimeSpan.FromMilliseconds(200))
        self.dataGrid.BeginAnimation(Grid.OpacityProperty,da)


    def dayBtn_MouseLeave(self,sender,e):
        day = str(int(str(sender.Name).split("_")[1])+1)
        sender.Content = day
        da = DoubleAnimation(100,TimeSpan.FromMilliseconds(200))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BeginAnimation(Button.WidthProperty,da)


    def dayBtn_MouseEnter(self,sender,e):
        day = int(str(sender.Name).split("_")[1])
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        if day in self.contractorDict.keys():
            data = self.contractorDict[day]
            try:
                advance = str(data['advance'])
                if id(advance.strip())!=id(""):
                    if float(advance)>0:
                        by_hand = str(data['by_hand']).strip()
                        if id(by_hand)!=id(""):
                            sender.Content = "Rs: {}, By: {}".format(advance,by_hand)
                        else:
                            sender.Content = "Rs: {}".format(advance)
                    else:
                        sender.Content = "Empty"
                else:
                    sender.Content = "Empty"
            except:
                sender.Content = "Empty"
        else:
            sender.Content = "Empty"
        da = DoubleAnimation(280,TimeSpan.FromMilliseconds(200))
        sender.BeginAnimation(Button.WidthProperty,da)

    def updateTotalAdvance(self):
        tot_rows = self.contractorDict['total_rows']
        tot_adv = 0.0
        tot_weight = 0.0
        for i in range(int(tot_rows)):
            if i in self.contractorDict.keys():
                row = self.contractorDict[i]
            else:
                row = self.contractorDict[str(i)]
            try:
                if id(str(row['advance']).strip())!=id(""):
                    tot_adv+= float(row['advance'])
            except:
                pass
            try:
                if id(str(row['weight']).strip())!=id(""):
                    tot_weight+= float(row['weight'])
            except:
                pass
        self.totalAdvanceLabel.Content = str(round(tot_adv))
        self.totalWeightLabel.Content = str(round(tot_weight))

    def insertBtn_Click(self,sender,e):
        date = str(self.dateLabel.Content)
        weight = str(self.weightText.Text)
        custName = str(self.custNameText.Text)
        advance = str(self.advanceText.Text)
        byHand = str(self.byHandText.Text)
        description = str(self.descriptionText.Text)

        self.contractorDict[self.current_day] = {'date':date,'weight':weight, 'cust_name':custName,
                                                'advance':advance,'by_hand':byHand,'description':description}
        self.dataGrid.Visibility = Visibility.Hidden
        self.updateTotalAdvance()


    def saveDataFile(self):
        data = self.contractorDict
        data['contractor_name'] = str(self.contractorNameText.Text).strip()
        data['phone_no'] = str(self.phoneNoText.Text).strip()
        data['team_of'] = str(self.teamOfText.Text).strip()
        data['rate'] = str(self.rateText.Text).strip()
        date_now = datetime.now().date()
        data['c_month'] = date_now.month
        data['c_year'] = date_now.year
        total_weight = 0
        total_advance = 0
        total_rows = int(data['total_rows'])
        for i in range(total_rows):
            if i in data.keys():
                bundle = data[i]
            elif str(i) in data.keys():
                bundle = data[str(i)]
            else:
                continue
            try:
                if id(str(bundle['weight']))!=id(""):
                    total_weight+=float(bundle['weight'])
                if id(str(bundle['advance']))!=id(""):
                    total_advance+=float(bundle['advance'])
            except:
                pass
        data['total_weight']=total_weight
        data['total_advance']=total_advance
        filename = str(data['month'])+"_"+str(data['year'])
        filename = encrypt(filename,self.key)
        if "filename" in data.keys():
            if str(data['filename']) != filename:
                filename = str(data['filename'])
        data['filename'] = filename
        file_path = "contractor/"+filename+".csai"
        if not os.path.isdir('contractor'):
            os.makedirs('contractor')
        with open(file_path, 'w') as fp:
            json.dump(data, fp)
        sync_data = "contractor\t"+filename+"\n"
        with open("sync_list.csai",'a') as fp:
            fp.write(sync_data)
        return filename

    def deleteWholeContractor_Click(self,sender,e):
        try:
            filename = self.contractorDict['filename'].split(".csai")[0]
            if filename != "":
                file_path = "contractor/"+filename+".csai"
                try:
                    os.remove(file_path)
                    with open("sync_list.csai",'a')as fp:
                        fp.write("del\tcontractor\t{}\n".format(filename))
                except:
                    pass
            self.Close()
            MessageBox.Show("Please update current status to Cloud Database...\n By clicking UPLOAD button...")
        except:
            self.Close()


    def pdfBtn_Click(self,sender,e):
        loadingWindow = LoadingWindow()
        loadingWindow.Show()
        self.Hide()
        filename=self.saveDataFile()
        args = ['ppython/python.exe', 'contractorPDF.py', 'contractor/{}'.format(filename)]
        process = run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            if int(process[0])==1:
                self.Show()
                loadingWindow.Close()
                del loadingWindow
                print(str(process))
                MessageBox.Show("Error while genrating PDF...")
            elif int(process[0])==0:
                form = WindowPDF()
                form.Show()
                loadingWindow.Close()
                del loadingWindow
                self.Close()
            else:
                MessageBox.Show("Error")
                print(str(process))
        except:
            MessageBox.Show("Error")

    
    def saveBtn_Click(self,sender,e):
        _ = self.saveDataFile()
        self.Close()


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
