import cv2
import numpy as np
import os

# Create Resources directory structure if it doesn't exist
os.makedirs('Resources/StudentDetailsArea', exist_ok=True)
os.makedirs('Resources/classOverview', exist_ok=True)

# Create placeholder images for StudentDetailsArea
student_detail_types = [
    "Already Marked Today",
    "Success - Attendance Marked", 
    "Loading...",
    "Unknown Person",
    "Waiting..."
]

for i, detail_type in enumerate(student_detail_types):
    # Create a 426x700 image
    img = np.ones((700, 426, 3), dtype=np.uint8) * 240  # Light gray background
    
    # Add colored header based on type
    if i == 0:  # Already marked
        cv2.rectangle(img, (0, 0), (426, 100), (0, 100, 200), -1)  # Orange-ish
    elif i == 1:  # Success
        cv2.rectangle(img, (0, 0), (426, 100), (0, 200, 0), -1)  # Green
    elif i == 2:  # Loading
        cv2.rectangle(img, (0, 0), (426, 100), (200, 200, 0), -1)  # Blue
    elif i == 3:  # Unknown
        cv2.rectangle(img, (0, 0), (426, 100), (0, 0, 200), -1)  # Red
    else:  # Waiting
        cv2.rectangle(img, (0, 0), (426, 100), (100, 100, 100), -1)  # Gray
    
    # Add text
    cv2.putText(img, detail_type, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Add placeholder for student photo (151x151)
    cv2.rectangle(img, (20, 80), (171, 231), (200, 200, 200), -1)
    cv2.putText(img, "Photo", (60, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
    
    # Add text areas
    cv2.putText(img, "Name:", (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "Roll No:", (20, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "Total Presents:", (20, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "Total Absents:", (20, 640), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "Attendance %:", (20, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Save the image
    cv2.imwrite(f'Resources/StudentDetailsArea/{i}.png', img)

# Create Background2.png (1280x720)
background = np.ones((720, 1280, 3), dtype=np.uint8) * 50  # Dark background
cv2.putText(background, "Face Attendance System", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
cv2.rectangle(background, (1270-320, 10), (1270, 10+240), (100, 100, 100), 2)  # Webcam area
cv2.putText(background, "Camera Feed", (1270-300, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
cv2.imwrite('Resources/Background2.png', background)

# Create classOverviewbackground2.png (427x700)
class_overview = np.ones((700, 427, 3), dtype=np.uint8) * 220  # Light background
cv2.rectangle(class_overview, (0, 0), (427, 60), (70, 130, 180), -1)  # Header
cv2.putText(class_overview, "Today's Attendance", (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
cv2.putText(class_overview, "Student ID          Status", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
cv2.imwrite('Resources/classOverview/classOverviewbackground2.png', class_overview)

print("Placeholder images created successfully!")
