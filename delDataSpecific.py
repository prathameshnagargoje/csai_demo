import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
from datetime import date,datetime
import sys

cred = credentials.Certificate('csai-demo-firebase-adminsdk-zqtm2-4677acfdd5.json')
firebase_admin.initialize_app(cred)

#9eQYEC1aJDWt7KtspOhHnr9yZtV2
#dwSiYZ9HkjwdZl5UL0C4

db = firestore.client()

def deleteData(days):
    folders = ['challan','bill','contractor']
    try:
        with open("log.csai",'w')as fp:
            fp.write("")
        days = str(days).split("\t")
        year = int(str(days[0]).strip())
        month = int(str(days[1]).strip())
        for folder in folders:
            docs = db.collection(folder).stream()
            for doc in docs:
                data = doc.to_dict()
                try:
                    if 'c_year' in data.keys():
                        if int(data['c_year'])==year:
                            if month == 13:
                                doc.reference.delete()
                            elif int(data['c_month'])==month:
                                doc.reference.delete()
                except Exception as e:
                    with open("log.csai",'a')as fp:
                        fp.write("\n\n{}\n\n".format(e))
    except Exception as e:
        with open("log.csai",'a')as fp:
            fp.write("\n\n{}\n\n".format(e))

if __name__ == "__main__":
    deleteData(*sys.argv[1:])