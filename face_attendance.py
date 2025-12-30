import pickle
import cv2 as cv
import os
import calendar
import face_recognition
import numpy as np
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

cred = credentials.Certificate("faceattendancesystem-c0163-firebase-adminsdk-bci46-64e225a7d7.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancesystem-c0163-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendancesystem-c0163.appspot.com'
})

bucket = storage.bucket()

WEBCAM_WIDTH, WEBCAM_HEIGHT = 640, 480
MY_WIDTH, MY_HEIGHT = 320, 240

camera_number = 1

capture = cv.VideoCapture(camera_number)
capture.set(3, WEBCAM_WIDTH)
capture.set(4, WEBCAM_HEIGHT)

background = cv.imread(r'Resources/Background2.png')

# student details area
studentDetailsPaths = os.listdir('Resources/StudentDetailsArea')
studentDetailsList = [cv.imread(os.path.join('Resources/StudentDetailsArea', path)) for path in studentDetailsPaths]

# month background
classOverview = cv.imread(r'Resources/classOverview/classOverviewbackground2.png')

current_date = datetime.now()
year = current_date.year
month = current_date.month
daysInTheMonth = calendar.monthrange(year, month)[1]

# loading encoded file
encodedfile = open('EncodedImages.p', 'rb')
encodedImagesWithIDs = pickle.load(encodedfile)
encodedfile.close()
encodedImages, studentIDs = encodedImagesWithIDs

stdID = -1
downloadCounter = 0
stdDetailType = 4

studentInformation = dict()
total_absents = 0
total_presents = 0
attendance_percentage = 0
name = ""
roll_no = 0
studentImage = []

prevStdId = -1

allStudentInformation = db.reference(f"Students").get()

while True:
    ret, frame = capture.read()
    if not ret:
        break

    frameSmall = cv.resize(frame, (0, 0), None, 0.25, 0.25)
    frameSmall = cv.cvtColor(frameSmall, cv.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(frameSmall)
    encodeFaceCurrentFrame = face_recognition.face_encodings(frameSmall, faceCurrentFrame)

    resized_frame = cv.resize(frame, (MY_WIDTH, MY_HEIGHT), interpolation=cv.INTER_AREA)
    background[10:10+MY_HEIGHT, 1270-MY_WIDTH:1270] = resized_frame

    if True:
        background[10:10+700, 10:10+426] = studentDetailsList[stdDetailType]

    if True:
        background[10:10+700, 426+30:426+30+427] = classOverview

    for encodeFace, faceLocation in zip(encodeFaceCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodedImages, encodeFace)
        faceDistance = face_recognition.face_distance(encodedImages, encodeFace)
        # print(f"faceDistance:\n{faceDistance}")

        minDistance = np.min(faceDistance)
        # print(f"Minimum dist: {minDistance}")

        if minDistance >= 0.5:
            downloadCounter = 0
            stdDetailType = 3
            continue

        matchedIndex = np.argmin(faceDistance)

        if matches[matchedIndex]:
            stdID = studentIDs[matchedIndex]

            if stdID != prevStdId:
                downloadCounter = 0

            prevStdId = stdID

            if downloadCounter == 0:
                downloadCounter = 1
                stdDetailType = 1

            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1*2, x2*2, y2*2, x1*2

            top_left = (1280-MY_WIDTH-10+x1, y1)
            bottom_right = (1280-MY_WIDTH-10+x2, y2+20)

            background = cv.rectangle(background, top_left, bottom_right, color=(0, 255, 0), thickness=1)

    if downloadCounter != 0:
        if downloadCounter == 1:
            ref = db.reference(f"Students/{stdID}")
            studentInformation = ref.get()
            
            last_attendance_time = studentInformation.get('last_attendance_time') # type: ignore
            if last_attendance_time:
                dateTimeObj = datetime.strptime(last_attendance_time, "%Y-%m-%d %H:%M:%S")
                last_attendance_date = dateTimeObj.date()
            else:
                last_attendance_date = None

            current_date = datetime.now().date()

            if last_attendance_date != current_date:  # Check if it's a new day
                studentInformation['total_presents'] += 1 # type: ignore
                studentInformation.setdefault('daily_attendance', {})[current_date.strftime("%Y-%m-%d")] = "present" # type: ignore
                ref.child('total_presents').set(studentInformation['total_presents']) # type: ignore
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                ref.child('daily_attendance').set(studentInformation['daily_attendance']) # type: ignore
            else:
                stdDetailType = 0
                counter = 0
                background[10:10+700, 10:10+426] = studentDetailsList[stdDetailType]

            name = studentInformation['name'] # type: ignore
            roll_no = stdID
            total_presents = studentInformation['total_presents'] # type: ignore
            total_absents = studentInformation['total_absents'] # type: ignore
            if total_absents != 0 or total_presents != 0:
                attendance_percentage = total_presents / (total_presents + total_absents) * 100

            allStudentInformation = db.reference(f"Students").get()
            blob = bucket.get_blob(f"Images/{stdID}.jpg")
            imgArray = np.frombuffer(blob.download_as_string(), np.uint8) # type: ignore
            studentImage = cv.imdecode(imgArray, cv.COLOR_BGRA2BGR)
            studentImage = cv.resize(studentImage, (151, 151))

        if 20 < downloadCounter < 40:
            stdDetailType = 0

        background[10:10+700, 10:10+426] = studentDetailsList[stdDetailType]

        cv.putText(background, str(name), (30, 59 + 151 + 70), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)
        cv.putText(background, str(roll_no), (30, 59 + 151 + 140), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
        cv.putText(background, str(total_presents), (426-128, 720-(59*3)), cv.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)
        cv.putText(background, str(total_absents), (426-128, 720-(59*2) + 10), cv.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)
        cv.putText(background, f"{attendance_percentage} %", (426-128, 720-(59) + 20), cv.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)

        

        background[80:80+151, 20:20+151] = studentImage

        downloadCounter += 1

        if downloadCounter >= 40:
            downloadCounter = 0
            stdDetailType = 4
            studentInformation = {}
            studentImage = []
            background[10:10+700, 10:10+426] = studentDetailsList[stdDetailType]
    
    cv.putText(background, datetime.now().date().strftime("%d/%m/%Y"), (1280-270, 310), cv.FONT_HERSHEY_DUPLEX, 1, (100, 30, 30), 1, cv.LINE_AA)
    yIncrement = 0
    for student_id, data in allStudentInformation.items(): # type: ignore
        today_date_str = current_date.strftime("%Y-%m-%d")
        today_attendance = data.get('daily_attendance', {}).get(today_date_str, "absent")  # <-- Update here
        text = f"{student_id}                   {str(today_attendance).capitalize()}"
        
        color = (0,0,0) # BGR
        if today_attendance == 'absent':
            color = (100,100,150) # BGR

        cv.putText(background, text, (427+50, 60+40+43+yIncrement), cv.FONT_HERSHEY_COMPLEX, 0.5, color, 1, cv.LINE_AA)
        yIncrement += 32
    cv.imshow('Attendance System', background)

    if cv.waitKey(1) & 0xFF == (ord('q') or ord('Q')):
        break

capture.release()
cv.destroyAllWindows()
