import cv2
import numpy as np
import os

# Create Images directory if it doesn't exist
os.makedirs('Images', exist_ok=True)

# Sample student data (using IDs from the sendDataToDatabase.py)
students = [
    ("F21BINCE1M04001", "Muhammad Abid"),
    ("F21BINCE1M04002", "M. Israr Khalil"),
    ("F21BINCE1M04004", "Abdul Hanan"),
    ("F21BINCE1M04007", "Faghia Qammar"),
    ("F21BINCE1M04008", "Muhammad Sameer Khan")
]

# Create sample face images (400x400 pixels for better face detection)
for i, (student_id, name) in enumerate(students):
    # Create a higher resolution base image
    img = np.ones((400, 400, 3), dtype=np.uint8) * 240  # Light background
    
    # Create a more realistic face shape (oval)
    face_center = (200, 200)
    face_axes = (90, 110)  # wider, taller oval
    cv2.ellipse(img, face_center, face_axes, 0, 0, 360, (220, 180, 150), -1)  # Face color
    
    # Add face contour
    cv2.ellipse(img, face_center, face_axes, 0, 0, 360, (200, 160, 130), 3)
    
    # Draw more realistic eyes
    left_eye_center = (170, 180)
    right_eye_center = (230, 180)
    
    # Eye shapes (elliptical)
    cv2.ellipse(img, left_eye_center, (12, 8), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(img, right_eye_center, (12, 8), 0, 0, 360, (255, 255, 255), -1)
    
    # Pupils
    cv2.circle(img, left_eye_center, 6, (50, 50, 50), -1)
    cv2.circle(img, right_eye_center, 6, (50, 50, 50), -1)
    
    # Iris highlights
    cv2.circle(img, (left_eye_center[0]-2, left_eye_center[1]-2), 2, (100, 100, 100), -1)
    cv2.circle(img, (right_eye_center[0]-2, right_eye_center[1]-2), 2, (100, 100, 100), -1)
    
    # Eyebrows
    cv2.ellipse(img, (170, 165), (15, 5), 0, 0, 180, (120, 80, 60), 3)
    cv2.ellipse(img, (230, 165), (15, 5), 0, 0, 180, (120, 80, 60), 3)
    
    # Nose - more detailed
    nose_points = np.array([[200, 190], [195, 210], [200, 215], [205, 210]], np.int32)
    cv2.fillPoly(img, [nose_points], (200, 160, 130))
    
    # Nostrils
    cv2.circle(img, (196, 212), 2, (180, 140, 110), -1)
    cv2.circle(img, (204, 212), 2, (180, 140, 110), -1)
    
    # Mouth - more realistic
    mouth_points = np.array([[185, 240], [200, 250], [215, 240]], np.int32)
    cv2.fillPoly(img, [mouth_points], (180, 100, 100))
    cv2.ellipse(img, (200, 245), (15, 6), 0, 0, 180, (160, 80, 80), 2)
    
    # Add some variation to make each face unique
    variation_color = (220 + i*5, 180 + i*3, 150 + i*2)
    cv2.circle(img, (150 + i*10, 200 + i*5), 3, variation_color, -1)
    
    # Add hair/head outline
    cv2.ellipse(img, (200, 160), (100, 80), 0, 180, 360, (100 + i*20, 60 + i*10, 30), -1)
    
    # Add student ID text at bottom
    cv2.putText(img, student_id, (50, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Save the image
    cv2.imwrite(f'Images/{student_id}.jpg', img)
    print(f"Created sample image for {name} ({student_id})")

print("\nSample student images created successfully!")
print("Note: These are placeholder images. Replace them with actual student photos for real usage.")
