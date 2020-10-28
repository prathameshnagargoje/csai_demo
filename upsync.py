import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
from datetime import date,datetime

cred = credentials.Certificate('csai-demo-firebase-adminsdk-zqtm2-4677acfdd5.json')
firebase_admin.initialize_app(cred)

#9eQYEC1aJDWt7KtspOhHnr9yZtV2
#dwSiYZ9HkjwdZl5UL0C4

db = firestore.client()


def uploadFile():
    data = ""
    with open("sync_list.csai",'r') as fp:
        data = fp.read()
    d1 = date(2000,1,1)
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    d1 = now.date() - d1
    data = data.split("\n")
    for i in data:
        try:
            i = i.split("\t")
            if str(i[0]).strip() == "del" and len(i)==3:
                folder = str(i[1])
                filename = str(i[2]).split("\n")[0]
                doc_ref = db.collection(folder).document(str(filename))
                doc_ref.delete()
            else:
                if len(i)==2:
                    folder = str(i[0])
                    filename = str(i[1]).split("\n")[0]
                    file_path = folder+"\\"+filename+".csai"
                    data_dict = {}
                    if os.path.exists(file_path):
                        with open(file_path,'r') as fp:
                            data_dict = json.load(fp)
                        
                        data_dict['timestamp_day'] = int(d1.days)
                        data_dict['timestamp_sec'] = int(seconds)
                        data_dict['uid'] = "9eQYEC1aJDWt7KtspOhHnr9yZtV2"
                        with open(file_path,'w')as fp:
                            json.dump(data_dict,fp)
                        doc_ref = db.collection(folder).document(str(filename))
                        doc_ref.set(data_dict)
        except Exception as e:
            print(e)

    with open("sync_list.csai",'w') as fp:
        fp.write("")
    
    
if __name__ == "__main__":
    uploadFile()
