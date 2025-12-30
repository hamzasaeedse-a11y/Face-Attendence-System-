import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

cred = credentials.Certificate("faceattendancesystem-c0163-firebase-adminsdk-bci46-64e225a7d7.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancesystem-c0163-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendancesystem-c0163.appspot.com'
})



allStudentInformation = db.reference(f"Students").get()


print(allStudentInformation)