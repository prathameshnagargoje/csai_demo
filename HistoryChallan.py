import wpf
from checkEncryption import *
from System.Windows import *
from System.Windows.Controls import Button,Grid
from System.Windows.Media import Brushes,Color,ColorConverter,SolidColorBrush
from System import TimeSpan
from System.Windows.Media.Animation import *
import os
import json
import random
import string
import sys
import subprocess
import re
from threading import Thread
from LoadingWindow import LoadingWindow
from WindowPDF import WindowPDF
from datetime import date,datetime
from ChallanPage import ChallanPage

class HistoryChallan(Window):
    key=""
    tot_cust = 0
    cust_files = {}
    month = ['--','Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
    sortByMonth = False
    sMonth = 0
    sYear = 0

    def windowClose(self,sender,e):
        while self.custList_stack.Children.Count>0:
            self.custList_stack.Children.RemoveAt(self.custList_stack.Children.Count-1)
        self.cust_files = {}
        self.tot_cust =0
        del self

    def __init__(selfBill,key):
        selfBill.key = key
        wpf.LoadComponent(selfBill, 'HistoryChallan.xaml')
        files = os.listdir("challan")
        selfBill.tot_cust=0
        selfBill.cust_files= {}
        while selfBill.custList_stack.Children.Count>0:
            selfBill.custList_stack.Children.RemoveAt(selfBill.custList_stack.Children.Count-1)
        for i in range(0,len(selfBill.month)):
            selfBill.monthComboBox.Items.Add(str(selfBill.month[i]))
        selfBill.monthComboBox.SelectedValue = str(selfBill.month[0])
        selfBill.yearComboBox.Items.Add("--")
        current_year = int(str(datetime.now().year).strip())
        for i in range(2020,current_year+1):
            selfBill.yearComboBox.Items.Add(str(i))
        selfBill.yearComboBox.SelectedValue = str("--")
        files = os.listdir("challan")
        for filename in files:
            data_dict = {}
            #cust_name = decrypt(str(filename.split(".csai")[0]),key)
            path = "{}\\{}".format("challan",str(filename))
            if os.path.isfile(path):
                with open(path, 'r') as fp:
                    data_dict=json.load(fp)
            cust_name = data_dict['cust_name']
            challan_no = str(data_dict['challan_no']).strip()

            try:
                newBtn = Button()
                newBtn.Content = "{} : {}".format(challan_no,str(cust_name).strip())
                newBtn.Name = str('Cust_'+str(selfBill.tot_cust))
                selfBill.cust_files[int(selfBill.tot_cust)] = {'c_month':data_dict['c_month'],'c_year':data_dict['c_year'],'filename': filename,'challan_no':challan_no, 'cust_name': str(cust_name), 'total_weight': data_dict['total_weight']}
                if "total_weight" in data_dict.keys():
                    newBtn.ToolTip = "Weight: {}".format(str(data_dict['total_weight']))
                else:
                    newBtn.ToolTip = ""
                newBtn.Height = 0
                newBtn.Width = 360
                newBtn.Margin = Thickness(3, 0, 3, 3)
                newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.FontSize = 18
                newBtn.Click += selfBill.custBtn_Click
                newBtn.MouseEnter+=selfBill.custBtn_MouseEnter
                newBtn.MouseLeave+=selfBill.custBtn_MouseLeave
                selfBill.custList_stack.Children.Add(newBtn)
                selfBill.tot_cust+=1
                da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                newBtn.BeginAnimation(Button.HeightProperty,da)
            except Exception as e:
                print(e)
        files = []

    def button_MouseEnter(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF2D3436"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))

    def button_MouseLeave(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
    
    def sortByDate(self,sender,e):
        self.monthComboBox.SelectedValue = "--"
        self.yearComboBox.SelectedValue = "--"
        self.sortByMonth = False
        self.tot_cust=0
        while self.custList_stack.Children.Count>0:
            self.custList_stack.Children.RemoveAt(self.custList_stack.Children.Count-1)
        for challan in self.cust_files:
            index = int(challan)
            challan = self.cust_files[challan]
            try:
                newBtn = Button()
                newBtn.Content = "{} : {}".format(str(challan['challan_no']),str(challan['cust_name']).strip())
                newBtn.Name = str('Cust_'+str(index))
                if "total_weight" in challan.keys():
                    newBtn.ToolTip = "Weight: {}".format(str(challan['total_weight']))
                else:
                    newBtn.ToolTip = ""
                newBtn.Height = 0
                newBtn.Width = 360
                newBtn.Margin = Thickness(3, 0, 3, 3)
                newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.FontSize = 18
                newBtn.Click += self.custBtn_Click
                newBtn.MouseEnter+=self.custBtn_MouseEnter
                newBtn.MouseLeave+=self.custBtn_MouseLeave
                self.custList_stack.Children.Add(newBtn)
                
                self.tot_cust += 1
                da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                newBtn.BeginAnimation(Button.HeightProperty,da)
            except Exception as e:
                print(e)

    def sortMonth_Click(self,sender,e):
        month = self.monthComboBox.SelectedValue
        year = self.yearComboBox.SelectedValue
        try:
            self.sortByMonth = True
            try:
                if id(str(month).strip())!=id("--"):
                    self.sMonth = self.month.index(month)
                else:
                    self.sMonth = 0
            except:
                self.sMonth = 0
            try:
                if id(str(year).strip())!=id("--"):
                    self.sYear = int(year)
                else:
                    self.sYear = 0
            except:
                self.sYear = 0
            self.tot_cust=0
            while self.custList_stack.Children.Count>0:
                self.custList_stack.Children.RemoveAt(self.custList_stack.Children.Count-1)
            if self.sMonth!=0 and self.sYear!=0:
                for challan in self.cust_files:
                    index = int(challan)
                    challan = self.cust_files[challan]
                    try:
                        if self.sYear == int(challan['c_year']):
                            if self.sMonth == int(challan['c_month']):
                                try:
                                    newBtn = Button()
                                    newBtn.Content = "{} : {}".format(str(challan['challan_no']),str(challan['cust_name']).strip())
                                    newBtn.Name = str('Cust_'+str(index))
                                    if "total_weight" in challan.keys():
                                        newBtn.ToolTip = "Weight: {}".format(str(challan['total_weight']))
                                    else:
                                        newBtn.ToolTip = ""
                                    newBtn.Height = 0
                                    newBtn.Width = 360
                                    newBtn.Margin = Thickness(3, 0, 3, 3)
                                    newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                                    newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                                    newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                                    newBtn.FontSize = 18
                                    newBtn.Click += self.custBtn_Click
                                    newBtn.MouseEnter+=self.custBtn_MouseEnter
                                    newBtn.MouseLeave+=self.custBtn_MouseLeave
                                    self.custList_stack.Children.Add(newBtn)
                                    
                                    self.tot_cust += 1
                                    da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                                    newBtn.BeginAnimation(Button.HeightProperty,da)
                                except Exception as e:
                                    print(e)
                    except Exception as e:
                        print(e)
            elif self.sYear!=0 and self.sMonth==0:
                for challan in self.cust_files:
                    index = int(challan)
                    challan = self.cust_files[challan]
                    try:
                        if self.sYear == int(challan['c_year']):
                            try:
                                newBtn = Button()
                                newBtn.Content = "{} : {}".format(str(challan['challan_no']),str(challan['cust_name']).strip())
                                newBtn.Name = str('Cust_'+str(index))
                                if "total_weight" in challan.keys():
                                    newBtn.ToolTip = "Weight: {}".format(str(challan['total_weight']))
                                else:
                                    newBtn.ToolTip = ""
                                newBtn.Height = 0
                                newBtn.Width = 360
                                newBtn.Margin = Thickness(3, 0, 3, 3)
                                newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                                newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                                newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                                newBtn.FontSize = 18
                                newBtn.Click += self.custBtn_Click
                                newBtn.MouseEnter+=self.custBtn_MouseEnter
                                newBtn.MouseLeave+=self.custBtn_MouseLeave
                                self.custList_stack.Children.Add(newBtn)
                                
                                self.tot_cust += 1
                                da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                                newBtn.BeginAnimation(Button.HeightProperty,da)
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
            else:
                self.sortByDate(None,None)
        except Exception as e:
            print(e)

    def custBtn_Click(self,sender,e):
        try:
            cust_no = int(str(sender.Name).split("_")[1])
            if cust_no in self.cust_files.keys():
                filename = self.cust_files[cust_no]
                filename = str(filename['filename'])
                form = ChallanPage(self.key,filename)
                form.Show()
                self.Close()
            elif str(cust_no) in self.cust_files.keys():
                filename = self.cust_files[str(cust_no)]
                filename = str(filename['filename'])
                form = ChallanPage(self.key,filename)
                form.Show()
                self.Close()
        except Exception as e:
            pass

    def custBtn_MouseLeave(self,sender,e):
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        if id(str(sender.ToolTip).strip())!=id(""):
            content = sender.Content
            sender.Content = str(sender.ToolTip)
            sender.ToolTip = str(content)

    def custBtn_MouseEnter(self,sender,e):
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        if id(str(sender.ToolTip).strip())!=id(""):
            content = sender.Content
            sender.Content = str(sender.ToolTip)
            sender.ToolTip = str(content)

