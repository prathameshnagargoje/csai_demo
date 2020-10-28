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
from datetime import date
from HistoryChallan import HistoryChallan
from HistoryBill import HistoryBill

class MainHistoryWindow(Window):
    key=""

    def __init__(selfHis,key):
        selfHis.key = key
        wpf.LoadComponent(selfHis, 'MainHistoryWindow.xaml')

    def billHis_btn_Click(self,sender,e):
        form = HistoryBill(self.key)
        form.Show()
        self.Close()

    def challanHis_btn_Click(self,sender,e):
        form = HistoryChallan(self.key)
        form.Show()
        self.Close()

    def button_MouseEnter(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FF2D3436"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))

    def button_MouseLeave(self,sender,e):
        sender.Background = SolidColorBrush(ColorConverter.ConvertFromString("#FFE65100"))
        sender.BorderBrush = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
        sender.Foreground = SolidColorBrush(ColorConverter.ConvertFromString("#FFF5F5F5"))
