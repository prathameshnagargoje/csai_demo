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
        days = int(str(days).strip())
        if days>0:
            for folder in folders:
                docs = db.collection(folder).stream()
                for doc in docs:
                    data = doc.to_dict()
                    if 'timestamp_day' in data.keys():
                        if int(data['timestamp_day'])<=int(days):
                            doc.reference.delete()
        else:
            for folder in folders:
                docs = db.collection(folder).stream()
                for doc in docs:
                    doc.reference.delete()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    deleteData(*sys.argv[1:])