import wpf
import os
import clr
clr.AddReference("Spire.Pdf")
clr.AddReference("Spire.PdfViewer.Forms")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Drawing import *
from Spire.Pdf import *
from Spire.PdfViewer.Forms import *
from Spire.PdfViewer import *
from Microsoft.Win32 import *
from System.IO import *
from System.Windows import *
from System.Windows.Documents import *
from System.Windows.Controls import *
from System.Windows.Media import *
#from System.Windows.Forms import *
from System import *
from System.Windows.Media.Animation import *
import sys
from System import Uri
import subprocess
import re

class WindowPDF(Window):
    pdfDocumentViewer1 = None
    img_counter=0

    def __init__(selfPDF,filepath=""):
        try:
            wpf.LoadComponent(selfPDF, 'WindowPDF.xaml')
            selfPDF.pdfDocumentViewer1 = None
            selfPDF.pdfDocumentViewer1 = PdfDocumentViewer()
            selfPDF.pdfDocumentViewer1.LoadFromFile("temp.pdf")
            pageCount = selfPDF.pdfDocumentViewer1.PageCount
            files = os.listdir("images")
            length = len(files)
            selfPDF.img_counter=length
            if pageCount>1:
                images = selfPDF.pdfDocumentViewer1.SaveAsImage(0,pageCount-1)
                j = selfPDF.img_counter
                for i in range(len(images)):
                    images[i].Save("images\\{}.bmp".format(str(j)))
                    j+=1
            else:
                images = selfPDF.pdfDocumentViewer1.SaveAsImage(0)
                images.Save("images\\{}.bmp".format(str(selfPDF.img_counter)))
            selfPDF.PagesContainer.Items.Clear()
            files = os.listdir("images")
            c_dir = os.getcwd()
            j = selfPDF.img_counter
            for filename in files:
                if j<len(files):
                    img = Image()
                    img.HorizontalAlignment = HorizontalAlignment.Center
                    img.Margin = Thickness(0, 4, 0, 4)
                    img.MaxWidth = 800
                    bmIMG = Imaging.BitmapImage()
                    bmIMG.BeginInit()
                    bmIMG.UriSource = Uri("{}/images/{}.bmp".format(c_dir,j))
                    bmIMG.EndInit()
                    img.Source = bmIMG
                    selfPDF.PagesContainer.Items.Add(img)
                    j+=1
                    del img
                    del bmIMG
        except Exception as e:
            print(e)

    def printBtn_Click(self,sender,e):
        try:
            self.pdfDocumentViewer1.PrintDoc()
        except Exception as e:
            print(e)


    def windowClosed(self,sender,e):
        self.PagesContainer.Items.Clear()
        del self.PagesContainer
        self.pdfDocumentViewer1.CloseDocument()
        del self.pdfDocumentViewer1
        self.Close()
        del self





