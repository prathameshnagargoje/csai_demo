from checkEncryption import *
import os
import json
from upsync import uploadFile
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

folders = ['bill','challan','contractor','sale_cust','service_cust']
key = "admin"

for folder in folders:
    files = os.listdir(folder)
    for filename in files:
        path = "{}/{}".format(folder,filename)
        if os.path.isfile(path):
            data = {}
            with open(path,'r')as fp:
                data = json.load(fp)
            newfname = ""

            if folder=="bill":
                newfname = str(data['invoice_no'])+"_"+str(data['cust_name'])
                newfname = encrypt(newfname,key)
            if folder=="challan":
                newfname = str(data['challan_no'])+"_"+str(data['cust_name'])
                newfname = encrypt(newfname,key)
            if folder=="contractor":
                newfname = str(data['month'])+"_"+str(data['year'])
                newfname = encrypt(newfname,key)
            if folder=="sale_cust":
                newfname = str(data['cust_name'])
                newfname = encrypt(newfname,key)
            if folder=="service_cust":
                newfname = str(data['cust_name'])
                newfname = encrypt(newfname,key)
            
            if newfname!=filename.split('.csai')[0]:
                print("\nDeleting...  {}\n".format(path))
                os.remove(path)
                with open('sync_list.csai','a')as fp:
                    fp.write("del\t{}\t{}\n".format(folder,filename.split('.csai')[0]))
            data['filename'] = newfname
            print("\nnew file {}/{}.csai\n".format(folder,newfname))
            with open('{}/{}.csai'.format(folder,newfname),'w')as fp:
                json.dump(data,fp)

if have_internet():
    uploadFile()
