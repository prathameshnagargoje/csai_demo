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
from datetime import date,datetime
from hashlib import sha256
try:
    import httplib
except:
    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

def subtract_years(dt, years):
    try:
        dt = dt.replace(year=dt.year-years)
    except ValueError:
        dt = dt.replace(year=dt.year-years, day=dt.day-1)
    d1 = date(2000,1,1)
    d1 = dt - d1
    return d1.day

class SettingsWindow(Window):
    month = ['--','Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']

    def __init__(selfSet):
        wpf.LoadComponent(selfSet, 'SettingsWindow.xaml')
        selfSet.yearCombo.Items.Add("--")
        current_year = int(str(datetime.now().year).strip())
        for i in range(2020,current_year+1):
            selfSet.yearCombo.Items.Add(str(i))
        selfSet.yearCombo.SelectedValue = str("--")

    def saveChallanInvoiceNo_Click(self,sender,e):
        try:
            cFlag = False
            iFlag = False
            challan_no = str(self.new_challan_text.Text).strip()
            if id(challan_no)!=id(""):
                challan_no = int(challan_no)
            if challan_no>0:
                cFlag = True
            else:
                MessageBox.Show("Error: Challan No. can not be 0.")
            invoice_no = str(self.new_invoice_text.Text).strip()
            if id(invoice_no)!=id(""):
                invoice_no = int(invoice_no)
            if invoice_no>0:
                iFlag = True
            else:
                MessageBox.Show("Error: Invoice No. can not be 0.")

            data = ""
            with open("data.csai",'r')as fp:
                data = fp.read()
            data = data.split("\n")
            strData = "{}\n".format(str(data[0]))
            if cFlag:
                strData+="{}\n".format(str(challan_no-1))
            if iFlag:
                strData += "{}\n".format(str(invoice_no-1))
            with open("data.csai",'w')as fp:
                fp.write(strData)
            MessageBox.Show("Challan and Invoice No. is updated...")
        except Exception as e:
            print(e)
        self.new_invoice_text.Text = ""
        self.new_challan_text.Text = ""
        

    def deleteData_Click(self,sender,e):
        loadingWindow = LoadingWindow()
        loadingWindow.Show()
        folders = ['challan','bill','contractor']
        delYear = str(self.delYear_text.Text).strip()
        delYear = int(delYear)
        days = 0
        if delYear>0:
            days = subtract_years(datetime.now(),delYear)
            try:
                for folder in folders:
                    filenames = os.listdir(folder)
                    for filename in filenames:
                        data = {}
                        with open("{}\\{}".format(folder,filename),'r')as fp:
                            data = json.load(fp)
                        
                        if "timestamp_day" in data.keys():
                            if data['timestamp_day']<=days:
                                os.remove("{}\\{}".format(folder,filename))
            except Exception as e:
                loadingWindow.Close()
                print(e)
        else:
            self.new_challan_text.Text = "1"
            self.new_invoice_text.Text = "1"
            for folder in folders:
                files = os.listdir(folder)
                try:
                    for filename in files:
                        os.remove("{}\\{}".format(folder,filename))
                except Exception as e:
                    print(e)
            self.saveChallanInvoiceNo_Click(None,None)
        if have_internet():
            args = ['ppython/python.exe', 'delData.py', '{}'.format(days)]
            process = run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                if int(process[0])==1:
                    loadingWindow.Close()
                    MessageBox.Show("Error...\n\n{}".format(str(process)))
                elif int(process[0])==0:
                    loadingWindow.Close()
                    MessageBox.Show("Online data deleted successfully...")
                else:
                    MessageBox.Show("Error...\n\n{}".format(str(process)))
            except:
                MessageBox.Show("Error...\n\n{}".format(str(process)))
        else:
            MessageBox.Show("Internet not connected... Online data deletion Failed...")
            loadingWindow.Close()
        del loadingWindow

    def button_MouseEnter(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF2D3436"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))

    def button_MouseLeave(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))

    def checkBox_Click(self,sender,e):
        content = str(sender.Content).strip()
        if content == "All":
            if sender.IsChecked:
                self.janCheck.IsChecked = True
                self.febCheck.IsChecked = True
                self.marCheck.IsChecked = True
                self.aprCheck.IsChecked = True
                self.mayCheck.IsChecked = True
                self.junCheck.IsChecked = True
                self.julyCheck.IsChecked = True
                self.augCheck.IsChecked = True
                self.sepCheck.IsChecked = True
                self.octCheck.IsChecked = True
                self.novCheck.IsChecked = True
                self.decCheck.IsChecked = True
            else:
                self.janCheck.IsChecked = False
                self.febCheck.IsChecked = False
                self.marCheck.IsChecked = False
                self.aprCheck.IsChecked = False
                self.mayCheck.IsChecked = False
                self.junCheck.IsChecked = False
                self.julyCheck.IsChecked = False
                self.augCheck.IsChecked = False
                self.sepCheck.IsChecked = False
                self.octCheck.IsChecked = False
                self.novCheck.IsChecked = False
                self.decCheck.IsChecked = False
        else:
            if not sender.IsChecked:
                self.allCheck.IsChecked = False
        
    
    def deleteSpecific_Click(self,sender,e):
        loadingWindow = LoadingWindow()
        loadingWindow.Show()
        folders = ['challan','bill','contractor']
        delYear = str(self.yearCombo.SelectedValue).strip()
        if delYear != "--":
            month=0
            if self.allCheck.IsChecked:
                month=13
            elif self.janCheck.IsChecked:
                month=1
            elif self.febCheck.IsChecked:
                month=2
            elif self.marCheck.IsChecked:
                month=3
            elif self.aprCheck.IsChecked:
                month=4
            elif self.mayCheck.IsChecked:
                month=5
            elif self.junCheck.IsChecked:
                month=6
            elif self.julyCheck.IsChecked:
                month=7
            elif self.augCheck.IsChecked:
                month=8
            elif self.sepCheck.IsChecked:
                month=9
            elif self.octCheck.IsChecked:
                month=10
            elif self.novCheck.IsChecked:
                month=11
            elif self.decCheck.IsChecked:
                month=12
            if month > 0:
                delYear = int(delYear)
                try:
                    for folder in folders:
                        filenames = os.listdir(folder)
                        for filename in filenames:
                            data = {}
                            with open("{}\\{}".format(folder,filename),'r')as fp:
                                data = json.load(fp)
                            if "c_year" in data.keys():
                                try:
                                    if int(data['c_year']) == delYear:
                                        if month == 13:
                                            os.remove("{}\\{}".format(folder,filename))
                                        elif int(data['c_month']) == month:
                                            os.remove("{}\\{}".format(folder,filename))
                                except Exception as e:
                                    print(e)
                except Exception as e:
                    loadingWindow.Close()
                    print(e)
                
                if have_internet():
                    args = ['ppython/python.exe', 'delDataSpecific.py', '{}\t{}'.format(delYear,month)]
                    process = run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    try:
                        if int(process[0])==1:
                            loadingWindow.Close()
                            MessageBox.Show("Error...\n\n{}".format(str(process)))
                        elif int(process[0])==0:
                            loadingWindow.Close()
                            MessageBox.Show("Online data deleted successfully...")
                        else:
                            MessageBox.Show("Error...\n\n{}".format(str(process)))
                    except:
                        MessageBox.Show("Error...\n\n{}".format(str(process)))
                        if os.path.isfile("log.csai"):
                            loadingWindow.Close()
                            MessageBox.Show("Error...\n\nLog is saved...")
                else:
                    MessageBox.Show("Internet not connected... Online data deletion Failed...")
            else:
                loadingWindow.Close()
                MessageBox.Show("Error: Month not Specified")
        else:
            loadingWindow.Close()
            MessageBox.Show("Error: Year is not selected")
        del loadingWindow

    def changeUsernamePassword_Click(self,sender,e):
        uname = str(self.uname_text.Text).strip()
        password = str(self.password_text.Text).strip()

        newStr = "{}{}".format(uname,password)
        h = sha256()
        h.update(bytes(newStr,'utf-8'))
        hash = h.hexdigest()
        data = ""
        with open("data.csai",'r')as fp:
            data = fp.read()
        data = data.split("\n")
        newData = "{}\n".format(str(hash))
        for i in range(1,len(data)):
            newData+="{}\n".format(str(data[i]))
        with open("data.csai",'w')as fp:
            fp.write(newData)

        MessageBox.Show("Username and Password changed successfully...")


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
