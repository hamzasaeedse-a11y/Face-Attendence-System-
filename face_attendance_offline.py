import pickle
import cv2 as cv
import os
import calendar
import face_recognition
import numpy as np
from datetime import datetime

# Offline version - no Firebase connection
print("Starting Face Attendance System (Offline Mode)")
print("Note: This version works without Firebase and saves data locally")

WEBCAM_WIDTH, WEBCAM_HEIGHT = 640, 480
MY_WIDTH, MY_HEIGHT = 320, 240

camera_number = 0  # Changed to 0 for most common camera

try:
    capture = cv.VideoCapture(camera_number)
    capture.set(3, WEBCAM_WIDTH)
    capture.set(4, WEBCAM_HEIGHT)
except Exception as e:
    print(f"Error accessing camera: {e}")
    print("Please ensure your camera is connected and not used by other applications")
    exit(1)

try:
    background = cv.imread(r'Resources/Background2.png')
    if background is None:
        print("Error: Could not load background image")
        exit(1)
except Exception as e:
    print(f"Error loading background: {e}")
    exit(1)

# Student details area
try:
    studentDetailsPaths = os.listdir('Resources/StudentDetailsArea')
    studentDetailsList = [cv.imread(os.path.join('Resources/StudentDetailsArea', path)) for path in studentDetailsPaths]
except Exception as e:
    print(f"Error loading student detail images: {e}")
    exit(1)

# Month background
try:
    classOverview = cv.imread(r'Resources/classOverview/classOverviewbackground2.png')
    if classOverview is None:
        print("Error: Could not load class overview image")
        exit(1)
except Exception as e:
    print(f"Error loading class overview: {e}")
    exit(1)

current_date = datetime.now()
year = current_date.year
month = current_date.month
daysInTheMonth = calendar.monthrange(year, month)[1]

# Loading encoded file
try:
    encodedfile = open('EncodedImages.p', 'rb')
    encodedImagesWithIDs = pickle.load(encodedfile)
    encodedfile.close()
    encodedImages, studentIDs = encodedImagesWithIDs
    print(f"Loaded encodings for {len(studentIDs)} students")
except Exception as e:
    print(f"Error loading face encodings: {e}")
    print("Please run: python encodeGenerator.py first")
    exit(1)

stdID = -1
downloadCounter = 0
stdDetailType = 4

# Local storage for offline mode
local_attendance = {}
for student_id in studentIDs:
    local_attendance[student_id] = {
        'name': f'Student {student_id}',
        'total_presents': 0,
        'total_absents': 0,
        'last_attendance_time': '2024-01-01 00:00:00',
        'daily_attendance': {}
    }

studentInformation = dict()
total_absents = 0
total_presents = 0
attendance_percentage = 0
name = ""
roll_no = 0
studentImage = []

prevStdId = -1

print("Face Attendance System Started - Press 'q' to quit")
print("Note: Attendance data will be saved locally")

while True:
    ret, frame = capture.read()
    if not ret:
        print("Failed to capture video frame")
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

        minDistance = np.min(faceDistance)

        if minDistance >= 0.5:
            downloadCounter = 0
            stdDetailType = 3  # Unknown person
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
            # Use local attendance data
            studentInformation = local_attendance[stdID]
            
            last_attendance_time = studentInformation.get('last_attendance_time')
            if last_attendance_time:
                dateTimeObj = datetime.strptime(last_attendance_time, "%Y-%m-%d %H:%M:%S")
                last_attendance_date = dateTimeObj.date()
            else:
                last_attendance_date = None

            current_date_obj = datetime.now().date()

            if last_attendance_date != current_date_obj:  # Check if it's a new day
                studentInformation['total_presents'] += 1
                studentInformation.setdefault('daily_attendance', {})[current_date_obj.strftime("%Y-%m-%d")] = "present"
                studentInformation['last_attendance_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save to local file
                with open('offline_attendance.txt', 'a') as f:
                    f.write(f"{stdID},{studentInformation['name']},{current_date_obj},present\n")
                
                print(f"Attendance marked for {stdID}")
            else:
                stdDetailType = 0  # Already marked
                counter = 0
                background[10:10+700, 10:10+426] = studentDetailsList[stdDetailType]

            name = studentInformation['name']
            roll_no = stdID
            total_presents = studentInformation['total_presents']
            total_absents = studentInformation['total_absents']
            if total_absents != 0 or total_presents != 0:
                attendance_percentage = total_presents / (total_presents + total_absents) * 100

            # Create a placeholder student image
            studentImage = np.ones((151, 151, 3), dtype=np.uint8) * 200
            cv.putText(studentImage, "Photo", (45, 80), cv.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)

        if 20 < downloadCounter < 40:
            stdDetailType = 0

        background[10:10+700, 10:10+426] = studentDetailsList[stdDetailType]

        cv.putText(background, str(name), (30, 59 + 151 + 70), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)
        cv.putText(background, str(roll_no), (30, 59 + 151 + 140), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
        cv.putText(background, str(total_presents), (426-128, 720-(59*3)), cv.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)
        cv.putText(background, str(total_absents), (426-128, 720-(59*2) + 10), cv.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)
        cv.putText(background, f"{attendance_percentage:.1f} %", (426-128, 720-(59) + 20), cv.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)

        background[80:80+151, 20:20+151] = studentImage

        downloadCounter += 1

        if downloadCounter >= 40:
            downloadCounter = 0
            stdDetailType = 4
            studentInformation = {}
            studentImage = []
            background[10:10+700, 10:10+426] = studentDetailsList[stdDetailType]
    
    cv.putText(background, datetime.now().date().strftime("%d/%m/%Y"), (1280-270, 310), cv.FONT_HERSHEY_DUPLEX, 1, (100, 30, 30), 1, cv.LINE_AA)
    
    # Display today's attendance from local data
    yIncrement = 0
    current_date_str = current_date.strftime("%Y-%m-%d")
    for student_id, data in local_attendance.items():
        today_attendance = data.get('daily_attendance', {}).get(current_date_str, "absent")
        text = f"{student_id}                   {str(today_attendance).capitalize()}"
        
        color = (0,0,0) # BGR
        if today_attendance == 'absent':
            color = (100,100,150) # BGR

        cv.putText(background, text, (427+50, 60+40+43+yIncrement), cv.FONT_HERSHEY_COMPLEX, 0.5, color, 1, cv.LINE_AA)
        yIncrement += 32

    cv.imshow('Attendance System (Offline)', background)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
print("Face Attendance System stopped")
print("Attendance data saved to 'offline_attendance.txt'")
