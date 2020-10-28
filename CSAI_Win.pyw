import wpf
from checkEncryption import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Media import *
from System import TimeSpan
from System.Windows.Media.Animation import *
import os
from System import *
import json
from ChallanPage import ChallanPage
from HistoryServiceCustomer import HistoryServiceCustomer
from HistorySaleCustomer import HistorySaleCustomer
from ContractorWindow import ContractorWindow
from BillWindow import BillWindow
from MainHistoryWindow import MainHistoryWindow
from HistoryServiceCustomer import HistoryServiceCustomer
from LoadingWindow import LoadingWindow
from SettingsWindow import SettingsWindow
import sys
import subprocess
import re
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

class MyWindow(Window):
    key = 'admin'
    challan_items_dict={}
    challan_current_item=''
    challan_current_bundle=0
    challan_current_bundleBtn = Button()
    isConnected = False


    if not os.path.exists("data.csai"):
        with open("data.csai",'w') as fp:
            fp.write("d82494f05d6917ba02f7aaa29689ccb444bb73f20380876cb05d1f37537b7892\n0\n0")
        MessageBox.Show("The data files has been corrupted...\n Please set new challan and invoice no. from settings...")

    if not os.path.exists("sync_list.csai"):
        with open("sync_list.csai",'a') as fp:
            fp.write("")

    def dateConvertor(self,date,flag='1'):
        date = date.split('-')
        if len(date)>1:
            date = str(date[2])+"-"+str(date[1])+"-"+str(date[0])
        else:
            date=''
        return date


    def __init__(self):
        wpf.LoadComponent(self, 'CSAI_Win.xaml')
        bmIMG = Imaging.BitmapImage()
        bmIMG.BeginInit()
        c_dir = os.getcwd()
        bmIMG.UriSource = Uri("{}/logo_csai.ico".format(c_dir))
        bmIMG.EndInit()
        self.Icon = bmIMG
        del bmIMG
        files = os.listdir("images")
        try:
            for filename in files:
                os.remove("images\\{}".format(filename))
        except Exception as e:
            print(e)
        if have_internet():
            self.connectionLabel.Content = "Connected !"
            self.connectionLabel.Width = 200
            self.isConnected = True
            self.downSync_btn_Click(None,None)
        else:
            self.connectionLabel.Content = "Not Connected !"
            self.connectionLabel.Width = 300
            self.isConnected = False
            MessageBox.Show("No Internet Connection...\n Downloading Failed...")

    def menuClosed(self,sender,e):
        try:
            if os.path.isfile("temp.pdf"):
                os.remove("temp.pdf")
            
            files = os.listdir("images")
            for filename in files:
                try:
                    os.remove("images/{}".format(filename))
                except:
                    pass
        except:
            pass

    def ifEnterHit(self,sender,e):
        try:
            if str(e.Key)=="Return":
                uname = str(self.username.Text).strip()
                password = str(self.password.Password).strip()
                if len(password)>0 and len(uname)>0:
                    self.LoginClick(None,None)
                else:
                    self.error_label.Content = 'Error: Password can not be blank...'
        except:
            pass
        
    def LoginClick(self,sender,e):
        username = self.username.Text
        password = self.password.Password
        if username=='' or password=='':
            self.error_label.Content = 'Error: Incorrect UserName or Password...'
        else:
            if checkEncryption(username,password):
                wpf.LoadComponent(self,'Window1.xaml')
                
            else:
                self.error_label.Content = 'Error: Incorrect UserName or Password...'

    
    def login_GotFocus(self, sender, e):
        self.error_label.Content = ''

    def button_MouseEnter(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF2D3436"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))

    def button_MouseLeave(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))

    def bill_btn_Click(self,sender,e):
        form = BillWindow(self.key)
        form.Show()

    def challan_btn_Click(self,sender,e):
        form = ChallanPage(self.key)
        form.Show()

    def contractor_btn_Click(self,sender,e):
        form = ContractorWindow(self.key)
        form.Show()

    def saleCustomer_btn_Click(self,sender,e):
        form = HistorySaleCustomer(self.key)
        form.Show()

    def serviceCustomer_btn_Click(self,sender,e):
        form = HistoryServiceCustomer(self.key)
        form.Show()

    def history_btn_Click(self,sender,e):
        form = MainHistoryWindow(self.key)
        form.Show()

    def sync_btn_Click(self,sender,e):
        loadingWindow = LoadingWindow()
        loadingWindow.Show()
        args = ['ppython/python.exe', 'upsync.py']
        process = run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            if int(process[0])==1:
                loadingWindow.Close()
                del loadingWindow
                MessageBox.Show("Error while uploading Data...\n\n{}".format(str(process)))
            elif int(process[0])==0:
                loadingWindow.Close()
                del loadingWindow
                MessageBox.Show("Data upload Successful")
            else:
                loadingWindow.Close()
                del loadingWindow
                print("Got something else...")
                print(str(process))
        except:
            loadingWindow.Close()
            del loadingWindow
            MessageBox.Show("Error...\n\n{}".format(str(process)))

    def downSync_btn_Click(self,sender,e):
        loadingWindow = LoadingWindow()
        loadingWindow.Show()
        args = ['ppython/python.exe', 'downsync.py']
        process = run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            if int(process[0])==1:
                loadingWindow.Close()
                del loadingWindow
                MessageBox.Show("Error while downloading Data...\n\n{}".format(str(process)))
            elif int(process[0])==0:
                loadingWindow.Close()
                del loadingWindow
                MessageBox.Show("Data Download Successful")
            else:
                loadingWindow.Close()
                del loadingWindow
                print("Got something else...")
                print(str(process))
        except:
            loadingWindow.Close()
            del loadingWindow
            MessageBox.Show("Error...\n\n{}".format(str(process)))

    def settingBtn_Click(self,sender,e):
        form = SettingsWindow()
        form.Show()

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


if __name__ == '__main__':
    Application().Run(MyWindow())
