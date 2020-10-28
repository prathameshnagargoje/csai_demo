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

class BillWindow(Window):
    key = ''
    bill_dict = {}
    tot_entry = 0
    bill_current_entry = 0

    def __init__(selfBill,key,filename=''):
        selfBill.key = key
        wpf.LoadComponent(selfBill, 'BillWindow.xaml')
        selfBill.displayGrid.Visibility = Visibility.Hidden
        selfBill.bill_dict={'tot_entry':0}
        selfBill.subTotalLabel.Content = "0.0"
        selfBill.bill_dict['invoice_no'] = selfBill.getNewBillNo()
        selfBill.invoice_no_label.Content = selfBill.bill_dict['invoice_no']
        selfBill.tot_entry=0
        try:
            if id(str(filename).strip())!= id(''):
                data_dict = {}
                with open("bill\\{}".format(filename),'r') as fp:
                    data_dict = json.load(fp)
                selfBill.invoice_no_label.Content = data_dict['invoice_no']
                selfBill.tot_entry = int(data_dict['tot_entry'])
                selfBill.transportText.Text = str(data_dict['transport'])
                selfBill.vehicle_noText.Text = str(data_dict['vehicle_no'])
                try:
                    selfBill.invoiceDate.SelectedDate = (datetime.strptime(str(data_dict['invoice_date']),"%d-%m-%Y")).date()
                except:
                    pass
                try:
                    selfBill.supplyDate.SelectedDate = (datetime.strptime(str(data_dict['supply_date']),"%d-%m-%Y")).date()
                except:
                    pass
                selfBill.customerNameText.Text = str(data_dict['cust_name'])
                selfBill.addressText.Text = str(data_dict['cust_address'])
                selfBill.stateText.Text = str(data_dict['cust_state'])
                selfBill.gstinText.Text = str(data_dict['cust_gstin'])
                selfBill.cgstText.Text = str(data_dict['cgst_per'])
                selfBill.sgstText.Text = str(data_dict['sgst_per'])
                selfBill.igstText.Text = str(data_dict['igst_per'])
                try:
                    selfBill.stateCodeText.Text = str(data_dict['state_code'])
                except:
                    selfBill.stateCodeText.Text = ""
                try:
                    selfBill.destinationText.Text = str(data_dict['destination'])
                except:
                    selfBill.destinationText.Text = ""
                selfBill.is_recipient.IsChecked = False
                for i in range(int(data_dict['tot_entry'])):
                    if str(i) in data_dict.keys():
                        data_dict[i] = data_dict[str(i)]
                        del data_dict[str(i)]
                selfBill.bill_dict = data_dict
                selfBill.updateSubTotalLabel()
                while selfBill.entryStack.Children.Count>0:
                    selfBill.entryStack.Children.RemoveAt(selfBill.entryStack.Children.Count-1)
                for i in range(0,selfBill.bill_dict['tot_entry']):
                    bundle = selfBill.bill_dict[i]
                    newBtn = Button()
                    newBtn.Content = str(i+1)
                    newBtn.Name = str('Entry_'+str(i))
                    newBtn.Height = 0
                    newBtn.Width = 100
                    newBtn.Margin = Thickness(3, 0, 3, 3)
                    newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                    newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                    newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                    newBtn.FontSize = 18
                    newBtn.Click += selfBill.viewBillEntry_Click
                    newBtn.MouseEnter+=selfBill.entryBtn_MouseEnter
                    newBtn.MouseLeave+=selfBill.entryBtn_MouseLeave
                    selfBill.entryStack.Children.Add(newBtn)
                    da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                    newBtn.BeginAnimation(Button.HeightProperty,da)
                selfBill.bill_current_entry = int(selfBill.bill_dict['tot_entry'])
                selfBill.displayGrid.Opacity = 1
                selfBill.displayGrid.Visibility = Visibility.Visible
                da = DoubleAnimation(0,TimeSpan.FromMilliseconds(200))
                selfBill.displayGrid.BeginAnimation(Grid.OpacityProperty,da)
                selfBill.updateSubTotalLabel()
                selfBill.displayGrid.Visibility = Visibility.Hidden
        except Exception as e:
            selfBill.Close()

    def ifEnterHit(self,sender,e):
        try:
            if str(e.Key).strip() == "Return":
                if len(str(self.weightText.Text).strip())>0 and len(str(self.priceText.Text).strip())>0:
                    self.save_Click(None,None)
        except:
            pass

    def getNewBillNo(self,flag='r'):
        f = open('data.csai','r')
        data = f.read().split()
        bill_no = int(data[2])+1
        data[2]=bill_no
        new_data = data[0]
        for i in range(1,len(data)):
            new_data+='\n'+str(data[i])
        f.close()
        if flag == 'w':
            f = open('data.csai','w')
            f.write(new_data)
            f.close()
        return bill_no
    
    def updateAmoundText(self,sender,e):
        price = str(self.priceText.Text).strip()
        weight = str(self.weightText.Text).strip()

        try:
            self.amountText.Text = str(float(price)*float(weight))
        except:
            pass

    def addEntry_Click(self,sender, e):
        try:
            tot_entry = int(self.tot_entry)
            newBtn = Button()
            newBtn.Content = str(tot_entry+1)
            newBtn.Name = str('Entry_'+str(tot_entry))
            newBtn.Height = 0
            newBtn.Width = 100
            newBtn.Margin = Thickness(3, 0, 3, 3)
            newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
            newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
            newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
            newBtn.FontSize = 18
            newBtn.Click += self.viewBillEntry_Click
            newBtn.MouseEnter+=self.entryBtn_MouseEnter
            newBtn.MouseLeave+=self.entryBtn_MouseLeave
            #setattr(self,str('Entry_'+str(tot_entry)),newBtn)
            self.entryStack.Children.Add(newBtn)
            entry = {'description':"",'hsncode':"",'qty':0,'weight':0,'price':0,'amount':0}
            self.bill_dict[tot_entry] = entry
            self.bill_dict['tot_entry']=tot_entry+1
            self.tot_entry += 1
            self.displayGrid.Visibility = Visibility.Hidden
            da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
            newBtn.BeginAnimation(Button.HeightProperty,da)
        except Exception as e:
            print(e)

    def button_MouseEnter(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF2D3436"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))

    def button_MouseLeave(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))

    def viewBillEntry_Click(self,sender,e):
        self.bill_current_entry=int(str(sender.Name).split('_')[1])
        self.bill_current_entryBtn = sender
        self.noLabel.Content = 'Entry No: '+str(self.bill_current_entry+1)
        entry = self.bill_dict[self.bill_current_entry]
        self.displayGrid.Visibility = Visibility.Visible
        da = DoubleAnimation(1,TimeSpan.FromMilliseconds(100))
        self.displayGrid.BeginAnimation(Grid.OpacityProperty,da)
        self.descGoodText.Text = str(entry['description'])
        self.hsnCodeText.Text = str(entry['hsncode'])
        self.qtyText.Text = str(entry['qty'])
        self.weightText.Text = str("{:.2f}".format(float(entry['weight'])))
        self.priceText.Text = str("{:.2f}".format(float(entry['price'])))
        self.amountText.Text = str("{:.2f}".format(float(entry['amount'])))
        del entry

    def entryBtn_MouseLeave(self,sender,e):
        da = DoubleAnimation(100,TimeSpan.FromMilliseconds(200))
        sender.BeginAnimation(Button.WidthProperty,da)
        sender.Content = str(int(str(sender.Name).split("_")[1])+1)
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))

    def entryBtn_MouseEnter(self,sender,e):
        da = DoubleAnimation(200,TimeSpan.FromMilliseconds(200))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BeginAnimation(Button.WidthProperty,da)
        entry = {}
        try:
            entry_no = int(str(sender.Name).split("_")[1])
            if entry_no in self.bill_dict.keys():
                entry = self.bill_dict[entry_no]
            else:
                entry = self.bill_dict[str(entry_no)]
        except:
            pass
        try:
            if len(str(entry['description']))>0 or float(entry['amount'])>0:
                sender.Content = '{} ->{:.0f}'.format(str(entry['description']),float(entry['amount']))
            elif float(entry['amount'])>0:
                sender.Content = 'amount: {:.0f}'.format(float(entry['amount']))
            elif len(str(entry['description']))>0:
                sender.Content = '{}'.format(str(entry['description']))
            else:
                sender.Content = 'Empty'
        except:
            sender.Content = 'Empty'

    def save_Click(self,sender,e):
        try:
            entry_no = self.bill_current_entry
            entry = {}
            if entry_no in self.bill_dict.keys():
                entry = self.bill_dict[entry_no]
            else:
                entry = self.bill_dict[str(entry_no)]
            entry['description'] = self.descGoodText.Text
            entry['hsncode'] = self.hsnCodeText.Text
            entry['qty'] = self.qtyText.Text
            entry['weight'] = self.weightText.Text
            entry['price'] = self.priceText.Text
            entry['amount'] = self.amountText.Text
            self.descGoodText.Text = ""
            self.hsnCodeText.Text = ""
            self.qtyText.Text = ""
            self.weightText.Text = ""
            self.priceText.Text = ""
            self.amountText.Text = ""
            da = DoubleAnimation(0,TimeSpan.FromMilliseconds(100))
            self.displayGrid.BeginAnimation(Grid.OpacityProperty,da)
            self.updateSubTotalLabel()
            self.displayGrid.Visibility = Visibility.Hidden
        except Exception as e:
            print(e)

    def delEntry_Click(self,sender,e):
        try:
            delEntry_no = self.bill_current_entry
            for i in range(int(self.bill_dict['tot_entry'])):
                if i==delEntry_no:
                    del self.bill_dict[i]
                if i>delEntry_no:
                    if i in self.bill_dict.keys():
                        self.bill_dict[i-1]=self.bill_dict[i]
            if i in self.bill_dict.keys():
                del self.bill_dict[i]
            self.bill_dict['tot_entry'] = int(self.bill_dict['tot_entry'])-1
            while self.entryStack.Children.Count>0:
                self.entryStack.Children.RemoveAt(self.entryStack.Children.Count-1)
            for i in range(0,self.bill_dict['tot_entry']):
                bundle = self.bill_dict[i]
                newBtn = Button()
                newBtn.Content = str(i+1)
                newBtn.Name = str('Entry_'+str(i))
                newBtn.Height = 0
                newBtn.Width = 100
                newBtn.Margin = Thickness(3, 0, 3, 3)
                newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#2d3436"))
                newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF3D00"))
                newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FF3D00"))
                newBtn.FontSize = 18
                newBtn.Click += self.viewBillEntry_Click
                newBtn.MouseEnter+=self.entryBtn_MouseEnter
                newBtn.MouseLeave+=self.entryBtn_MouseLeave
                self.entryStack.Children.Add(newBtn)
                da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                newBtn.BeginAnimation(Button.HeightProperty,da)
            self.bill_current_entry = int(self.bill_dict['tot_entry'])
            self.displayGrid.Opacity = 1
            self.displayGrid.Visibility = Visibility.Visible
            da = DoubleAnimation(0,TimeSpan.FromMilliseconds(200))
            self.displayGrid.BeginAnimation(Grid.OpacityProperty,da)
            self.updateSubTotalLabel()
            self.displayGrid.Visibility = Visibility.Hidden
        except Exception as e:
            print(e)

    def updateSubTotalLabel(self):
        try:
            data_dict = self.bill_dict
            tot_entry = int(data_dict['tot_entry'])
            tot_amount = 0.0
            for i in range(0,tot_entry):
                entry = {}
                if i in data_dict.keys():
                    entry = data_dict[i]
                else:
                    entry = data_dict[str(i)]
                if id(str(entry['amount']).strip()) != id(''):
                    tot_amount+=float(entry['amount'])
            self.subTotalLabel.Content = "{:.2f}".format(float(tot_amount))
        except Exception as e:
            print(e)

    def saveData(self):
        data_dict = self.bill_dict
        invoice_no = self.getNewBillNo()
        if invoice_no==data_dict['invoice_no']:
            invoice_no = self.getNewBillNo('w')
        data_dict['transport'] = str(self.transportText.Text).strip()
        data_dict['vehicle_no'] = str(self.vehicle_noText.Text).strip()
        data_dict['invoice_date'] = str(self.invoiceDate.SelectedDate).strip().split(' ')[0]
        data_dict['supply_date'] = str(self.supplyDate.SelectedDate).strip().split(' ')[0]
        data_dict['cust_name'] = str(self.customerNameText.Text).strip()
        data_dict['cust_address'] = str(self.addressText.Text).strip()
        data_dict['cust_state'] = str(self.stateText.Text).strip()
        data_dict['cust_gstin'] = str(self.gstinText.Text).strip()
        data_dict['cgst_per'] = str(self.cgstText.Text).strip()
        data_dict['sgst_per'] = str(self.sgstText.Text).strip()
        data_dict['igst_per'] = str(self.igstText.Text).strip()
        data_dict['state_code'] = str(self.stateCodeText.Text).strip()
        data_dict['destination'] = str(self.destinationText.Text).strip()
        data_dict['counter'] = int(data_dict['tot_entry'])
        date_now = datetime.now().date()
        data_dict['c_month'] = date_now.month
        data_dict['c_year'] = date_now.year

        if self.is_recipient.IsChecked:
            data_dict['if_copy'] = "F"
        else:
            data_dict['if_copy'] = "T"

        try:
            self.updateSubTotalLabel()
            tot_amount = float(self.subTotalLabel.Content)
        except Exception as e:
            print(e)
        try:
            data_dict['cgst_total'] = (float(tot_amount)*float(data_dict['cgst_per']))/100
        except:
            data_dict['cgst_total']=0
        try:
            data_dict['sgst_total'] = (float(tot_amount)*float(data_dict['sgst_per']))/100
        except:
            data_dict['sgst_total']=0
        try:
            data_dict['igst_total'] = (float(tot_amount)*float(data_dict['igst_per']))/100
        except:
            data_dict['igst_total']=0

        data_dict['grand_total']= data_dict['cgst_total']+data_dict['sgst_total']+data_dict['igst_total']+float(tot_amount)

        #------------TimeStamp Var------------------
        

        #print(str(data_dict))
        filename = str(data_dict['invoice_no'])+"_"+str(data_dict['cust_name'])
        filename = encrypt(filename,self.key)
        if "filename" in data_dict.keys():
            if str(data_dict['filename']) != filename:
                filename = str(data_dict['filename'])
        data_dict['filename'] = filename
        path = "bill/{}.csai".format(filename)
        with open(path, 'w') as fp:
            json.dump(data_dict, fp)

        sync_data = "bill\t"+filename+"\n"
        with open("sync_list.csai",'a') as fp:
            fp.write(sync_data)

        return data_dict,filename

    def billSaveBtn_Click(self,sender,e):
        _,_ = self.saveData()
        self.Close()

    def billGetPDFBtn_Click(self,sender,e):
        self.displayGrid.Visibility = Visibility.Hidden
        loadingWindow = LoadingWindow()
        loadingWindow.Show()
        self.Hide()
        data,filename=self.saveData()
        args = ['ppython/python.exe', 'billPDF.py', 'bill/{}'.format(filename)]
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

    def deleteWholeBill_Click(self,sender,e):
        try:
            filename = self.bill_dict['filename'].split(".csai")[0]
            if filename != "":
                file_path = "bill/"+filename+".csai"
                try:
                    os.remove(file_path)
                    with open("sync_list.csai",'a')as fp:
                        fp.write("del\tbill\t{}\n".format(filename))
                except:
                    pass
            self.Close()
            MessageBox.Show("Please update current status to Cloud Database...\n By clicking UPLOAD button...")
        except:
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