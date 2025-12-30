import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("faceattendancesystem-c0163-firebase-adminsdk-bci46-64e225a7d7.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancesystem-c0163-default-rtdb.firebaseio.com/'
})

reference = db.reference('Students')
data = {
    "F21BINCE1M04001": {
        "name": "Muhammad Abid",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04002": {
        "name": "M. Israr Khalil",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04004": {
        "name": "Abdul Hanan",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04007": {
        "name": "Faghia Qammar",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04008": {
        "name": "Muhammad Sameer Khan",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04012": {
        "name": "Muhammad Ahsan Zafar",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04015": {
        "name": "Abdullah Yaqoob",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04016": {
        "name": "Nasir Naseer Naseer",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04017": {
        "name": "Hamza Rauf",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04019": {
        "name": "Abdul Aziz",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04026": {
        "name": "Muhammad Hassam Chuhan",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04028": {
        "name": "Sobia Bibi",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04034": {
        "name": "Nauman Saleem",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04035": {
        "name": "Tamjeela Shabeer",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04036": {
        "name": "Dawood Bilal",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04039": {
        "name": "Sikander Azam",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "F21BINCE1M04040": {
        "name": "Faheem Ahmad",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    },
    "S21BISR1M03009": {
        "name": "Aghoosh Rizvi",
        "total_presents": 0,
        "total_absents": 0,
        "last_attendance_time":"2024-01-01 00:00:00",
        "daily_attendance": {}
    }
}



for i, j in data.items():
    reference.child(i).set(j)