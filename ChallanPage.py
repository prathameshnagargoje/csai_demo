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

class ChallanPage(Window):
    key = ''
    challan_items_dict={}
    challan_current_item=''
    challan_current_bundle=0
    challan_current_bundleBtn = Button()
    filename = ""

    def __init__(selfChallan,key,filename=""):
        selfChallan.key = key
        wpf.LoadComponent(selfChallan, 'ChallanPage.xaml')
        selfChallan.challanBundleListGrid.Visibility = Visibility.Hidden
        selfChallan.challanBundleGrid.Visibility = Visibility.Hidden
        selfChallan.challanDeleteGrid.Visibility = Visibility.Hidden
        selfChallan.tot_weight_lable.Content = "0.0"
        selfChallan.challan_no_label.Content = selfChallan.getNewChallanNo()
        selfChallan.challan_items_dict={}
        selfChallan.challan_current_item=''
        selfChallan.challan_current_bundle=0
        selfChallan.challan_current_bundleBtn = Button()
        if id(str(filename).strip())!=id(""):
            data_dict = {}
            try:
                with open("challan\\{}".format(filename),'r') as fp:
                    data_dict = json.load(fp)
                selfChallan.challanDeleteGrid.Visibility = Visibility.Hidden
                selfChallan.challanBundleGrid.Visibility = Visibility.Hidden
                selfChallan.challanBundleListGrid.Visibility = Visibility.Hidden
                #=============================================
                selfChallan.customer_name.Text = str(data_dict['cust_name']).strip()
                selfChallan.challan_no_label.Content = str(data_dict['challan_no']).strip()
                selfChallan.vehicle_no.Text = str(data_dict['vehicle_no']).strip()
                try:
                    if 'cust_name' in data_dict.keys():
                        del data_dict['cust_name']
                    if 'challan_no' in data_dict.keys():
                        del data_dict['challan_no']
                    if 'vehicle_no' in data_dict.keys():
                        del data_dict['vehicle_no']
                    if 'total_weight' in data_dict.keys():
                        del data_dict['total_weight']
                    if 'c_month' in data_dict.keys():
                        del data_dict['c_month']
                    if 'c_year' in data_dict.keys():
                        del data_dict['c_year']
                    if 'timestamp_sec' in data_dict.keys():
                        del data_dict['timestamp_sec']
                    if 'timestamp_day' in data_dict.keys():
                        del data_dict['timestamp_day']
                    if 'uid' in data_dict.keys():
                        del data_dict['uid']
                    if 'filename' in data_dict.keys():
                        selfChallan.filename = data_dict['filename']
                        del data_dict['filename']
                    else:
                        selfChallan.filename = filename.split('.csai')[0]
                except Exception as e:
                    print(e)
                for i in range(int(data_dict['tot_items'])):
                    if i in data_dict.keys():
                        item = data_dict[i]
                        del data_dict[i]
                    else:
                        item = data_dict[str(i)]
                        del data_dict[str(i)]
                    for j in range(int(item['tot_bundles'])):
                        if str(j) in item.keys():
                            bundle = item[str(j)]
                            del item[str(j)]
                            item[j] = bundle
                    data_dict[item['item_name']] = item
                del data_dict['tot_items']
                selfChallan.challan_items_dict = data_dict
                #=============================================
                while selfChallan.item_list_panel.Children.Count>0:
                    selfChallan.item_list_panel.Children.RemoveAt(selfChallan.item_list_panel.Children.Count-1)
                for item in selfChallan.challan_items_dict:
                    try:
                        item = selfChallan.challan_items_dict[item]
                        newBtn = Button()
                        newBtn.Content = item['item_name']
                        letters = string.ascii_lowercase
                        letters = ''.join(random.choice(letters) for i in range(8))
                        newBtn.Name = letters
                        newBtn.ToolTip = item['item_name']
                        newBtn.Height = 0
                        newBtn.Width = 257
                        newBtn.Margin = Thickness(3, 0, 3, 3)
                        newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                        newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                        newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                        newBtn.FontSize = 18
                        newBtn.Click += selfChallan.showItem
                        newBtn.MouseEnter+=selfChallan.itemBtn_MouseEnter
                        setattr(selfChallan,item['item_name']+"_Btn",newBtn)
                        newBtn.MouseLeave+=selfChallan.itemBtn_MouseLeave
                        selfChallan.item_list_panel.Children.Add(newBtn)
                        da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                        newBtn.BeginAnimation(Button.HeightProperty,da)
                        selfChallan.item_name_text.Text = ''
                    except Exception as e:
                        MessageBox.Show("Error: \n\n{}".format(e))
                selfChallan.calculateTotalWeight()
            except:
                selfChallan.Close()

    def getNewChallanNo(self,flag='r'):
            f = open('data.csai','r')
            data = f.read().split()
            challan_no = int(data[1])+1
            data[1]=challan_no
            new_data = data[0]
            for i in range(1,len(data)):
                new_data+='\n'+str(data[i])
            f.close()
            if flag == 'w':
                f = open('data.csai','w')
                f.write(new_data)
                f.close()
            return challan_no

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

    def addItem_btn_Click(self,sender,e):
        itemName = str(self.item_name_text.Text).strip()
        if id(itemName)!=id(""):
            if not itemName in self.challan_items_dict.keys():
                newBtn = Button()
                newBtn.Content = itemName
                letters = string.ascii_lowercase
                letters = ''.join(random.choice(letters) for i in range(8))
                newBtn.Name = letters
                newBtn.ToolTip = itemName
                newBtn.Height = 0
                newBtn.Width = 257
                newBtn.Margin = Thickness(3, 0, 3, 3)
                newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
                newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
                newBtn.FontSize = 18
                newBtn.Click += self.showItem
                newBtn.MouseEnter+=self.itemBtn_MouseEnter
                newBtn.MouseLeave+=self.itemBtn_MouseLeave
                setattr(self,itemName+"_Btn",newBtn)
                self.item_list_panel.Children.Add(newBtn)
                self.item_name_text.Text = ''
                self.challan_items_dict[itemName]={'item_name':itemName,'tot_bundles':0}
                self.challanDeleteGrid.Visibility = Visibility.Hidden
                self.challanBundleGrid.Visibility = Visibility.Hidden
                da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
                newBtn.BeginAnimation(Button.HeightProperty,da)
            else:
                MessageBox.Show("Items can not have same Names...")
        else:
            MessageBox.Show("Item Name can not be Blank...")
        self.item_name_text.Text = ''


    def showItem(self,sender,e):
        itemName = ""
        data = {}
        if sender!=None:
            itemName = str(sender.ToolTip)
        else:
            itemName = self.challan_current_item
        while self.items_bundle_stack.Children.Count>0:
            self.items_bundle_stack.Children.RemoveAt(self.items_bundle_stack.Children.Count-1)
        self.challanBundleGrid.Visibility = Visibility.Hidden
        self.challanDeleteGrid.Visibility = Visibility.Hidden
        if itemName in self.challan_items_dict.keys():
            data = self.challan_items_dict[itemName]
        else:
            self.challan_items_dict[itemName]={'item_name':itemName,'tot_bundles':0}
            data = {'item_name':itemName,'tot_bundles':0}
        for i in range(0,data['tot_bundles']):
            if i in data.keys():
                bundle = data[i]
            else:
                bundle = data[str(i)]
            newBtn = Button()
            newBtn.Content = str(i+1)
            newBtn.Name = str('bundleBtn_'+str(i))
            newBtn.Height = 0
            newBtn.Width = 100
            newBtn.Margin = Thickness(3, 0, 3, 3)
            newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
            newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
            newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
            newBtn.FontSize = 18
            newBtn.Click += self.viewChallanBundle
            newBtn.MouseEnter+=self.bundleBtn_MouseEnter
            newBtn.MouseLeave+=self.bundleBtn_MouseLeave
            self.items_bundle_stack.Children.Add(newBtn)
            da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
            newBtn.BeginAnimation(Button.HeightProperty,da)
        self.challan_current_bundle = int(data['tot_bundles'])
        self.challan_current_item=itemName
        self.itemNameLabel.Content = itemName
        self.challanBundleListGrid.Opacity = 0
        self.challanBundleListGrid.Visibility = Visibility.Visible
        da = DoubleAnimation(1,TimeSpan.FromMilliseconds(200))
        self.challanBundleListGrid.BeginAnimation(Grid.OpacityProperty,da)
        del data

    def itemBtn_MouseLeave(self,sender,e):
        sender.Content = str(sender.ToolTip)
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))

    def itemBtn_MouseEnter(self,sender,e):
        itemName = str(sender.ToolTip)
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        tot_weight = 0.0
        tot_bun = 0
        try:
            if itemName in self.challan_items_dict.keys():
                item= self.challan_items_dict[itemName]
                bundle_cc = int(item['tot_bundles'])
                tot_bun = bundle_cc
                for i in range(bundle_cc):
                    bundle = {}
                    if i in item.keys():
                        bundle = item[i]
                    elif str(i) in item.keys():
                        bundle = item[str(i)]
                    else:
                        continue
                    try:
                        if id(str(bundle['gross_wt']).strip())!=id(""):
                            tot_weight+=float(bundle['gross_wt'])
                    except:
                        pass
        except:
            pass
        sender.Content = "{}, wt: {:.0f}".format(int(tot_bun),float(tot_weight))


    def bundleBtn_MouseLeave(self,sender,e):
        da = DoubleAnimation(100,TimeSpan.FromMilliseconds(200))
        sender.BeginAnimation(Button.WidthProperty,da)
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Content = str(int(str(sender.Name).split("_")[1])+1)
    
    def bundleBtn_MouseEnter(self,sender,e):
        da = DoubleAnimation(210,TimeSpan.FromMilliseconds(200))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BeginAnimation(Button.WidthProperty,da)
        try:
            bundle_no = int(str(sender.Name).split("_")[1])
            if self.challan_current_item in self.challan_items_dict.keys():
                bundle = self.challan_items_dict[self.challan_current_item]
                if bundle_no in bundle.keys():
                    bundle = bundle[bundle_no]
                else:
                    bundle = bundle[str(bundle_no)]
        except:
            pass
        try:
            if float(bundle['qty'])!=0 or float(bundle['gross_wt'])!=0:
                sender.Content = '{:.0f}, {:.2f}'.format(float(bundle['qty']),float(bundle['gross_wt']))
            else:
                sender.Content = 'Empty'
        except:
            sender.Content = 'Empty'

    def addNewBundleChallan(self,sender,e):
        itemName = self.challan_current_item
        tot_bundle = self.challan_items_dict[itemName]
        tot_bundle = int(tot_bundle['tot_bundles'])
        newBtn = Button()
        newBtn.Content = str(tot_bundle+1)
        letters = string.ascii_lowercase
        letters = ''.join(random.choice(letters) for i in range(8))
        newBtn.Name = str('Item_'+str(tot_bundle)+'_bundleBtn')
        newBtn.Height = 0
        newBtn.Width = 100
        newBtn.Margin = Thickness(3, 0, 3, 3)
        newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        newBtn.FontSize = 18
        newBtn.Click += self.viewChallanBundle
        newBtn.MouseEnter+=self.bundleBtn_MouseEnter
        newBtn.MouseLeave+=self.bundleBtn_MouseLeave
        setattr(self,str('Item_'+str(tot_bundle)+'_bundleBtn'),newBtn)
        self.items_bundle_stack.Children.Add(newBtn)
        bundle = {'qty':0,'gross_wt':0}
        item = self.challan_items_dict[itemName]
        item[tot_bundle] = bundle
        item['tot_bundles']=tot_bundle+1
        self.challan_items_dict[itemName] = item
        self.challanBundleGrid.Visibility = Visibility.Hidden
        self.challanDeleteGrid.Visibility = Visibility.Hidden
        da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
        newBtn.BeginAnimation(Button.HeightProperty,da)
        del item
        
    def viewChallanBundle(self,sender,e):
        self.challan_current_bundle=int(str(sender.Name).split('_')[1])
        self.challan_current_bundleBtn = sender
        itemName = self.challan_current_item
        self.bundleCounterLabel.Content = 'Bundle No: '+str(self.challan_current_bundle+1)
        item = self.challan_items_dict[itemName]
        if self.challan_current_bundle in item.keys():
            bundle = item[self.challan_current_bundle]
        else:
            bundle = item[str(self.challan_current_bundle)]
        self.challanDeleteGrid.Opacity = 1
        da = DoubleAnimation(0,TimeSpan.FromMilliseconds(100))
        self.challanDeleteGrid.BeginAnimation(Grid.OpacityProperty,da)
        self.challanDeleteGrid.Visibility = Visibility.Hidden
        self.challanBundleGrid.Opacity = 0
        self.challanBundleGrid.Visibility = Visibility.Visible
        da = DoubleAnimation(1,TimeSpan.FromMilliseconds(100))
        self.challanBundleGrid.BeginAnimation(Grid.OpacityProperty,da)
        if  bundle['qty']!=0 or bundle['gross_wt']!=0:
            self.qty_text.Text = str(bundle['qty'])
            self.gross_wt_text.Text = str(bundle['gross_wt'])
        else:
            self.qty_text.Text = ''
            self.gross_wt_text.Text = ''
        del item
        del bundle
        
    def insertRowInChallanDataGrid(self,sender,e):
        itemName = self.challan_current_item
        bundle_no = self.challan_current_bundle
        try:
            if str(self.qty_text.Text)!='' and str(self.qty_text.Text)!='-':
                qty = '{:.2f}'.format(float(self.qty_text.Text))
            else:
                qty = 0
            if str(self.gross_wt_text.Text)!='' and str(self.gross_wt_text.Text)!='-':
                gross_wt = '{:.2f}'.format(float(self.gross_wt_text.Text))
            else:
                gross_wt = 0
            item = self.challan_items_dict[itemName]
            item[bundle_no]={'qty':qty,'gross_wt':gross_wt}
            self.challan_items_dict[itemName] = item
        except:
            pass
        self.challanBundleGrid.Opacity = 1
        da = DoubleAnimation(0,TimeSpan.FromMilliseconds(100))
        self.challanBundleGrid.BeginAnimation(Grid.OpacityProperty,da)
        self.challanBundleGrid.Visibility = Visibility.Hidden
        self.calculateTotalWeight()
        del item

    def calculateTotalWeight(self):
        tot_weight = 0.0
        for i in self.challan_items_dict:
            item = self.challan_items_dict[i]
            tot_bundle = int(item['tot_bundles'])
            for j in range(0,tot_bundle):
                if j in item.keys():
                    bundle = item[j]
                elif str(j) in item.keys():
                    bundle = item[str(j)]
                else:
                    continue
                try:
                    tot_weight+=float("{:.2f}".format(float(bundle['gross_wt'])))
                except:
                    pass
        self.tot_weight_lable.Content = str("{:.2f}".format(float(tot_weight)))

    def challanSaveData(self):
        try:
            data = {}
            cc=0
            challan_no = int(self.challan_no_label.Content)
            tot_weight = 0
            cust_name = str(self.customer_name.Text)
            vehicle_no = str(self.vehicle_no.Text)
            try:
                for item in self.challan_items_dict:
                    item = self.challan_items_dict[item]
                    if 'tot_bundles' in item.keys():
                        tot_bundle = item['tot_bundles']
                        tot_qty=0
                        tot_gross_wt = 0
                        if int(tot_bundle)>0:
                            for i in range(0,int(tot_bundle)):
                                if i in item.keys():
                                    bundle = item[i]
                                    if str(bundle['qty'])!='' and str(bundle['qty'])!='-':
                                        try:
                                            tot_qty+=float(bundle['qty'])
                                        except:
                                            pass
                                    if str(bundle['gross_wt'])!='' and str(bundle['gross_wt'])!='-':
                                        try:
                                            tot_gross_wt+=float(bundle['gross_wt'])
                                        except:
                                            pass
                                else:
                                    bundle = item[str(i)]
                                    if str(bundle['qty'])!='' and str(bundle['qty'])!='-':
                                        try:
                                            tot_qty+=float(bundle['qty'])
                                        except:
                                            pass
                                    if str(bundle['gross_wt'])!='' and str(bundle['gross_wt'])!='-':
                                        try:
                                            tot_gross_wt+=float(bundle['gross_wt'])
                                        except:
                                            pass
                            item['tot_qty']='{:.2f}'.format(float(tot_qty))
                            item['tot_gross_wt']='{:.2f}'.format(float(tot_gross_wt))
                            tot_weight+=tot_gross_wt
                            data[cc]=item
                            cc+=1
            except Exception as e:
                print(e)
            data['tot_items']=cc
            data['cust_name']=cust_name
            data['vehicle_no']=vehicle_no
            data['challan_no']=challan_no
            data['total_weight']='{:.2f}'.format(float(tot_weight))
            date_now = datetime.now().date()
            data['c_month'] = date_now.month
            data['c_year'] = date_now.year
            filename = str(data['challan_no']).strip()+"_"+str(data['cust_name']).strip()
            filename = encrypt(filename,self.key)
            if self.filename != "":
                if self.filename != filename:
                    filename = self.filename
            data['filename'] = filename
            file_path = "challan/"+filename+".csai"
            if not os.path.isdir('challan'):
                os.makedirs('challan')
            with open(file_path, 'w') as fp:
                json.dump(data, fp)
            sync_data = "challan\t"+filename+"\n"
            with open("sync_list.csai",'a') as fp:
                fp.write(sync_data)
            #write challan no to file
            latest_challan_no = self.getNewChallanNo()
            if int(challan_no)==int(latest_challan_no):
                challan_no = self.getNewChallanNo(str('w'))
            return data,filename
        except Exception as e:
            print(e)

    def deleteBtn_Click(self,sender,e):
        self.insertRowInChallanDataGrid(sender,e)
        itemName = self.challan_current_item
        item = self.challan_items_dict[itemName]
        bundle_cc = int(item['tot_bundles'])
        self.bundleCombo.Items.Clear()
        for i in range(bundle_cc):
            self.bundleCombo.Items.Add(str(i+1))
        self.challanDeleteGrid.Opacity = 0
        self.challanDeleteGrid.Visibility = Visibility.Visible
        da = DoubleAnimation(1,TimeSpan.FromMilliseconds(100))
        self.challanDeleteGrid.BeginAnimation(Grid.OpacityProperty,da)


    def deleteBundleBtn_Click(self,sender,e):
        delBun_index = str(self.bundleCombo.SelectedValue)
        try:
            delBun_index = int(delBun_index)-1
            itemName = self.challan_current_item
            item = self.challan_items_dict[itemName]
            for i in range(int(item['tot_bundles'])):
                if i==delBun_index:
                    del item[i]
                if i>delBun_index:
                    if i in item.keys():
                        item[i-1]=item[i]
            if i in item.keys():
                del item[i]
            item['tot_bundles'] = int(item['tot_bundles'])-1
            self.challan_items_dict[itemName]=item
            with open('Log.txt','w') as log:
                log.write(str(self.challan_items_dict))
            self.challanDeleteGrid.Opacity = 1
            da = DoubleAnimation(0,TimeSpan.FromMilliseconds(100))
            self.challanDeleteGrid.BeginAnimation(Grid.OpacityProperty,da)
            self.challanDeleteGrid.Visibility = Visibility.Hidden
            newBtn = getattr(self,str('Item_'+str(delBun_index)+'_bundleBtn'))
            da = DoubleAnimation(0,TimeSpan.FromMilliseconds(100))
            newBtn.BeginAnimation(Button.HeightProperty,da)
        except:
            pass
        self.calculateTotalWeight()
        self.showItem(None,e)


    def deleteItemBtn_Click(self,sender,e):
        itemName = self.challan_current_item
        newBtn = getattr(self,itemName+"_Btn")
        da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
        newBtn.BeginAnimation(Button.HeightProperty,da)
        del self.challan_items_dict[itemName]
        self.challanDeleteGrid.Visibility = Visibility.Hidden
        self.challanBundleGrid.Visibility = Visibility.Hidden
        self.challanBundleListGrid.Visibility = Visibility.Hidden
        while self.item_list_panel.Children.Count>0:
            self.item_list_panel.Children.RemoveAt(self.item_list_panel.Children.Count-1)
        for item in self.challan_items_dict:
            newBtn = Button()
            newBtn.Content = item
            letters = string.ascii_lowercase
            letters = ''.join(random.choice(letters) for i in range(8))
            newBtn.Name = letters
            newBtn.ToolTip = item
            newBtn.Height = 0
            newBtn.Width = 257
            newBtn.Margin = Thickness(3, 0, 3, 3)
            newBtn.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
            newBtn.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
            newBtn.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
            newBtn.FontSize = 18
            newBtn.Click += self.showItem
            newBtn.MouseEnter+=self.itemBtn_MouseEnter
            newBtn.MouseLeave+=self.itemBtn_MouseLeave
            self.item_list_panel.Children.Add(newBtn)
            da = DoubleAnimation(35,TimeSpan.FromMilliseconds(100))
            newBtn.BeginAnimation(Button.HeightProperty,da)
            self.item_name_text.Text = ''
        self.calculateTotalWeight()


    def deleteWholeChallan_Click(self,sender,e):
        try:
            filename = self.filename.split(".csai")[0]
            if filename != "":
                file_path = "challan/"+filename+".csai"
                try:
                    os.remove(file_path)
                    with open("sync_list.csai",'a')as fp:
                        fp.write("del\tchallan\t{}\n".format(filename))
                except:
                    pass
            self.Close()
            MessageBox.Show("Please update current status to Cloud Database...\n By clicking UPLOAD button...")
        except:
            self.Close()
        


    def challanSaveBtn_Click(self,sender,e):
        if id(str(self.customer_name.Text).strip())==id(""):
            self.customer_name.Text="-"
        if id(str(self.vehicle_no.Text).strip())==id(""):
            self.vehicle_no.Text="-"
        _,_ = self.challanSaveData()
        self.Close()

    def ifEnterHit(self,sender,e):
        try:
            if str(e.Key).strip() == "Return":
                self.addItem_btn_Click(None,None)
        except:
            pass

    def ifEnterHitBundle(self,sender,e):
        try:
            if str(e.Key).strip() == "Return":
                self.insertRowInChallanDataGrid(None,None)
        except:
            pass
        

    def challanGetPDFBtn_Click(self,sender,e):
        self.challanBundleListGrid.Visibility = Visibility.Hidden
        self.challanMainGrid.Visibility = Visibility.Hidden
        self.challanBundleGrid.Visibility = Visibility.Hidden
        self.challanDeleteGrid.Visibility = Visibility.Hidden
        loadingWindow = LoadingWindow()
        loadingWindow.Show()
        self.Hide()
        if id(str(self.customer_name.Text).strip())==id(""):
            self.customer_name.Text="-"
        if id(str(self.vehicle_no.Text).strip())==id(""):
            self.vehicle_no.Text="-"
        data,filename=self.challanSaveData()
        args = ['ppython/python.exe', 'challanPDF.py', 'challan/{}'.format(filename)]
        process = run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            if int(process[0])==1:
                self.challanBundleListGrid.Visibility = Visibility.Visible
                self.challanMainGrid.Visibility = Visibility.Visible
                self.challanBundleGrid.Visibility = Visibility.Visible
                self.challanDeleteGrid.Visibility = Visibility.Hidden
                self.Show()
                loadingWindow.Close()
                MessageBox.Show("Error while genrating PDF...")
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
