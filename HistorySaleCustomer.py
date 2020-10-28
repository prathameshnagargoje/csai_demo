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
from datetime import date
from SaleCustomerWindow import SaleCustomerWindow

class HistorySaleCustomer(Window):
    key = ""
    tot_cust = 0
    total_rembal=0
    cust_files = {}

    def __init__(hscSelf,key):
        hscSelf.key = key
        wpf.LoadComponent(hscSelf, 'HistorySaleCustomer.xaml')
        hscSelf.tot_cust = 0
        files = os.listdir("sale_cust")
        while hscSelf.custList_stack.Children.Count>0:
            hscSelf.custList_stack.Children.RemoveAt(hscSelf.custList_stack.Children.Count-1)
        for filename in files:
            data_dict = {}
            #cust_name = decrypt(str(filename.split(".csai")[0]),key)
            path = "{}\\{}".format("sale_cust",str(filename))
            if os.path.isfile(path):
                with open(path, 'r') as fp:
                    data_dict=json.load(fp)
            try:
                cust_name = data_dict['cust_name']
                rembal = data_dict['total_rembal']
                try:
                    if id(str(rembal).strip())!=id(""):
                        hscSelf.total_rembal+=float(rembal)
                except:
                    pass
                tot_cust = int(hscSelf.tot_cust)
                newBtn = Button()
                newBtn.Content = str(cust_name).strip()
                newBtn.Name = str('Cust_'+str(tot_cust))
                hscSelf.cust_files[int(tot_cust)] = {'filename': filename, 'cust_name': str(cust_name), 'rembal': rembal}
                newBtn.ToolTip = "Rem Bal: {}".format(str(rembal))
                newBtn.Height = 0
                newBtn.Width = 360
                newBtn.Margin = Thickness(3, 0, 3, 3)
                newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.FontSize = 18
                newBtn.Click += hscSelf.custBtn_Click
                newBtn.MouseEnter+=hscSelf.custBtn_MouseEnter
                newBtn.MouseLeave+=hscSelf.custBtn_MouseLeave
                hscSelf.custList_stack.Children.Add(newBtn)
                
                hscSelf.tot_cust += 1
                da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                newBtn.BeginAnimation(Button.HeightProperty,da)
            except Exception as e:
                print(e)
        try:
            hscSelf.totRemBalLabel.Content = "{:.0f}".format(float(hscSelf.total_rembal))
        except:
            pass

    def button_MouseEnter(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF2D3436"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))

    def button_MouseLeave(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))


    def custBtn_Click(self,sender,e):
        cust_no = int(str(sender.Name).split("_")[1])
        if cust_no in self.cust_files.keys():
            data = self.cust_files[cust_no]
            filename = str(data['filename'])
            form = SaleCustomerWindow(self.key,filename)
            form.Show()
            self.Close()
    
    def findCust_Click(self,sender,e):
        fcust_name = str(self.cust_Text.Text).strip().lower()
        while self.custList_stack.Children.Count>0:
            self.custList_stack.Children.RemoveAt(self.custList_stack.Children.Count-1)
        for i in range(0,len(self.cust_files)):
            try:
                if i in self.cust_files.keys():
                    cust = self.cust_files[i]
                else:
                    cust = self.cust_files[str(i)]
                cust_name = str(cust['cust_name']).strip()
                if cust_name.lower().find(fcust_name) != -1:
                    rembal = cust['rembal']
                    newBtn = Button()
                    newBtn.Content = str(cust_name).strip()
                    newBtn.Name = str('Cust_'+str(i))
                    newBtn.ToolTip = "Rem Bal: {}".format(str(rembal))
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
                    
                    da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                    newBtn.BeginAnimation(Button.HeightProperty,da)
            except Exception as e:
                print(e)

    def clearFind_Click(self,sender,e):
        self.cust_Text.Text = ""
        while self.custList_stack.Children.Count>0:
            self.custList_stack.Children.RemoveAt(self.custList_stack.Children.Count-1)
        for i in range(0,len(self.cust_files)):
            try:
                if i in self.cust_files.keys():
                    cust = self.cust_files[i]
                else:
                    cust = self.cust_files[str(i)]
                cust_name = str(cust['cust_name']).strip()
                rembal = cust['rembal']
                newBtn = Button()
                newBtn.Content = str(cust_name).strip()
                newBtn.Name = str('Cust_'+str(i))
                newBtn.ToolTip = "Rem Bal: {}".format(str(rembal))
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
                
                da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                newBtn.BeginAnimation(Button.HeightProperty,da)
            except Exception as e:
                print(e)

    def custBtn_MouseLeave(self,sender,e):
        content = sender.Content
        sender.Content = str(sender.ToolTip)
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.ToolTip = str(content)

    def custBtn_MouseEnter(self,sender,e):
        content = sender.Content
        sender.Content = str(sender.ToolTip)
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.ToolTip = str(content)


    def newCustomerBtn_Click(self,sender,e):
        form = SaleCustomerWindow(self.key)
        form.Show()
        self.Close()
