from fileinput import filename
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


cred = credentials.Certificate("faceattendancesystem-c0163-firebase-adminsdk-bci46-64e225a7d7.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancesystem-c0163-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendancesystem-c0163.appspot.com'
})


studentFacesPaths = os.listdir('Images')
# print(f"Path: \n {studentFacesPaths}")

for path in studentFacesPaths:
    fileName = f"Images/{path}"
    
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
