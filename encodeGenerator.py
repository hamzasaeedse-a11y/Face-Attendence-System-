import cv2 as cv
import face_recognition
import pickle
import os


# student face images
studentFacesPaths = os.listdir('Images')

studentFacesList = []
studentIDs =[]

for path in studentFacesPaths:
    studentFacesList.append(cv.imread(os.path.join('Images', path)))
    studentIDs.append(os.path.splitext(path)[0])


def doEncoding(images):
    encodeList = []
    valid_ids = []
    
    for i, img in enumerate(images):
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img_rgb)
        
        if len(face_encodings) > 0:
            encode = face_encodings[0]
            encodeList.append(encode)
            valid_ids.append(studentIDs[i])
            print(f"✓ Face detected and encoded for {studentIDs[i]}")
        else:
            print(f"✗ No face detected in image for {studentIDs[i]}")
    
    return encodeList, valid_ids



print("Encoding ... please wait ... ")
encodedImages, validIDs = doEncoding(studentFacesList)

if len(encodedImages) > 0:
    encodedImagesWithIDs = [encodedImages, validIDs]
    print(f"Encoding complete for {len(encodedImages)} faces")
    
    file = open('EncodedImages.p', 'wb')
    pickle.dump(encodedImagesWithIDs, file)
    file.close()
    print("File saved")
    print(f"Valid student IDs: {validIDs}")
else:
    print("No faces were detected in any images. Please check your image files.")
